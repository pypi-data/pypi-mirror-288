#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import os
import sys
import argparse
import hashlib
import shutil
import time
import datetime
import subprocess
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from asn1crypto import cms, tsp

OID_TIMESTAMP_TOKEN = '1.2.840.113549.1.9.16.1.4'
OID_SHA256 = '2.16.840.1.101.3.4.2.1'
TSA_POLICY = '1.2.3.4.1'

def load_cert(cert_path):
    with open(cert_path, "rb") as f:
        cert_bytes = f.read()
        cert = None
        try:
            cert = x509.load_pem_x509_certificate(cert_bytes)
        except ValueError:
            cert = x509.load_der_x509_certificate(cert_bytes)
        return cert

def load_priv(priv_path, passwd=None):
    with open(priv_path, "rb") as f:
        priv_bytes = f.read()
        key = None
        try:
            key = serialization.load_pem_private_key(priv_bytes, passwd)
        except ValueError:
            key = serialization.load_der_private_key(priv_bytes, passwd)
        return key

def sign_cms_pss(cafile,
                 cakey, 
                 signerCA,
                 signerCRL,
                 rootCRL,
                 tssigner,
                 tskey,
                 tsCA,
                 timestamp,
                 file_name):

    if shutil.which('java') is None:
        print('FATAL: Please install java!!!')
        return

    try:
        if timestamp is None:
            timestamp = ""
        module_path = os.path.dirname(__file__)
        cmd = ['java', '-jar', f'{module_path}/cmssign-1.0-SNAPSHOT.jar',
                '--signer', cafile,
                '--key', cakey,
                '--signerCA', signerCA,
                '--signerCRL', signerCRL,
                '--rootCRL', rootCRL,
                '--tssigner', tssigner,
                '--tskey', tskey,
                '--tsCA', tsCA,
                '--timestamp', timestamp,
                '-src', file_name]
        print(f'cmd = [{" ".join(cmd)}]')
        ret = subprocess.Popen(cmd)
        ret.wait()
        print(f'Output = [{file_name}.p7s]')
    except Exception as e:
        print(f'FATAL: sign with pass failed: {e}')

def sign_cms(cafile, cakey, file_name):
    cert = load_cert(cafile)
    key = load_priv(cakey)
    content = None
    with open(file_name, "rb") as f:
        content = f.read()
    opt = [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.Binary, pkcs7.PKCS7Options.NoCapabilities]
    cms_bytes = pkcs7.PKCS7SignatureBuilder().set_data(content).add_signer(cert, key, hashes.SHA256()).sign(serialization.Encoding.DER, opt)

    return cms_bytes

def get_cms_signature_hash(cms_bytes):
    cms_info = cms.ContentInfo.load(cms_bytes)
    cms_content = cms_info['content']
    cms_signature = cms_content['signer_infos'][0]['signature'].native
    return cms_signature

def get_time(timestr):
    if len(timestr) == len("20010101"):
        try:
            timestamp = datetime.datetime.strptime(timestr, "%Y%m%d")
            return timestamp
        except ValueError as e:
            raise ValueError(f"timestamp[{timestr}]format error")
    if len(timestr) == len("20010101010101"):
        try:
            timestamp = datetime.datetime.strptime(timestr, "%Y%m%d%H%M%S")
            return timestamp
        except ValueError as e:
            raise ValueError(f"timestamp[{timestr}]format error")
    raise ValueError(f"timestamp[{timestr}]format error")

def sign_tsa(cms_bytes, file_name, tsca_file, tskey_file, timestampstr = None):
    """
    sign for time stamp query
    """
    cms_info = cms.ContentInfo.load(cms_bytes)
    cms_content = cms_info['content']
    cms_signature = cms_content['signer_infos'][0]['signature'].native
    tshash = hashlib.sha256(cms_signature).digest()

    timestamp = datetime.datetime.now()
    if timestampstr is not None:
        timestamp = get_time(timestampstr)

    with open(f"{file_name}.hash", "wb+") as f:
        f.write(cms_signature)

    seconds = int(time.mktime(timestamp.timetuple()))
    cmssign.ts.query(f'{file_name}.hash', f'{file_name}.tsq')
    cmssign.ts.reply(f'{file_name}.tsq', f'{file_name}.tsr', tsca_file, tskey_file, seconds)

    with open(f'{file_name}.tsr', 'rb') as f:
        return f.read()
    return None

def append_tsa_to_cms(cms_bytes, tsa_bytes):
    info = cms.ContentInfo.load(cms_bytes)
    cms_content = info['content']

    ts = tsp.TimeStampResp.load(tsa_bytes)
    ts_token = ts['time_stamp_token']
    content = cms.SetOfContentInfo()
    content.append(ts_token)
    attribute = cms.CMSAttribute()
    attribute['type'] = 'signature_time_stamp_token'
    attribute['values'] = content
    attrs = cms.CMSAttributes()
    attrs.append(attribute)
    cms_content['signer_infos'][0]['unsigned_attrs'] = attrs
    info['content'] = cms_content
    return info.dump()

def sign(args):
    if not os.path.exists(args.infile):
        print(f"FATAL: file to sign is not exist! file=[{args.infile}]")
        sys.exit(-1)

    if not os.path.exists(args.cafile) or not os.path.exists(args.cakey):
        print("FATAL: certificate or private key is not exist")
        sys.exit(-1)

    if len(args.outfile) == 0:
        args.outfile = f'{args.infile}.cms'

    cert = load_cert(args.cafile)
    if 'PSS' in cert.signature_algorithm_oid._name.upper():
        return sign_cms_pss(args.cafile,
                            args.cakey, 
                            args.signerCA,
                            args.signerCRL,
                            args.rootCRL,
                            args.tssigner,
                            args.tskey,
                            args.tsCA,
                            args.timestamp,
                            args.infile)

    try:
        cms_bytes = sign_cms(args.cafile, args.cakey, args.infile)
        if os.path.exists(args.tsca) and os.path.exists(args.tskey):
            tsa_bytes = sign_tsa(cms_bytes, args.infile, args.tsca, args.tskey, args.timestamp)
            big_cms = append_tsa_to_cms(cms_bytes, tsa_bytes)
            print("INFO: add timestamp signature to cms file success")
        else:
            print("WARN: timestamp certificate or private key is not set, no timestamp signature")
            big_cms = cms_bytes

        with open(args.outfile, 'wb+') as f:
            f.write(big_cms)
        print(f"INFO: sign success. output={args.outfile}")
    except Exception as e:
        print(f"FATAL: sign failed. error={e}")

def combine(args):
    cms_bytes = None
    tsa_bytes = None
    with open(args.cmsfile, 'rb') as f:
        cms_bytes = f.read()
    with open(args.tsfile, 'rb') as f:
        tsa_bytes = f.read()

    big_cms = append_tsa_to_cms(cms_bytes, tsa_bytes)
    with open(args.outfile, 'wb+') as f:
        f.write(big_cms)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help or run cmssignui with GUI support')

    parser_sign = subparsers.add_parser('sign')
    parser_sign.add_argument('--signer', dest='cafile', required=True, type=str, default='',
                             help='signer certificate file, DER format')
    parser_sign.add_argument('--key', dest='cakey', required=True, type=str, default='', help='signer private key')
    parser_sign.add_argument('--signerCA', dest='signerCA', required=False, type=str, default='',
                             help='CA of signer, DER format')
    parser_sign.add_argument('--signerCRL', dest='signerCRL', required=False, type=str, default='',
                             help='CRL of signer, DER format')
    parser_sign.add_argument('--rootCRL', dest='rootCRL', required=False, type=str, default='',
                             help='CRL of root CA, DER format')
    parser_sign.add_argument('--tssigner', dest='tssigner', type=str, default='',
                             help='timestamp signer certificate, DER format')
    parser_sign.add_argument('--tskey', dest='tskey', type=str, default='',
                             help='timestamp signer private key, DER format')
    parser_sign.add_argument('--tsCA', dest='tsCA', type=str, default='',
                             help='CA of timestamp signer, DER format')
    parser_sign.add_argument('--timestamp', dest='timestamp', type=str, default=None,
                             help="timestamp. use system time if not set. format must be '20220101123000' yyyyMMDDHHMMSS")
    parser_sign.add_argument('--in', dest='infile', required=True, type=str, default='', help='file to sign')
    parser_sign.add_argument('--out', dest='outfile', type=str, default='', help='output file')
    parser_sign.set_defaults(func=sign)

    parser_combine = subparsers.add_parser('combine')
    parser_combine.add_argument('--cmsfile', dest='cmsfile', required=True, type=str, default='', help='cms file')
    parser_combine.add_argument('--tsfile', dest='tsfile', required=True, type=str, default='', help='timestamp file')
    parser_combine.add_argument('--out', dest='outfile', required=True, type=str, default='', help='output file')
    parser_combine.set_defaults(func=combine)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(-1)
    args.func(args)

if __name__ == '__main__':
    main()
