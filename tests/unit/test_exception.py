__author__ = "Nitin Kumar, Rick Sherman"
__credits__ = "Jeremy Schulman"

import unittest
from nose.plugins.attrib import attr
from jnpr.junos.exception import RpcError, CommitError, \
    ConnectError, ConfigLoadError, RpcTimeoutError
from jnpr.junos import Device
from lxml import etree


commit_xml = '''
        <rpc-error xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:junos="http://xml.juniper.net/junos/12.1X46/junos" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <error-severity>error</error-severity>
        <source-daemon>dcd</source-daemon>
        <error-path>[edit interfaces ge-0/0/1]</error-path>
        <error-info>
        <bad-element>unit 2</bad-element>
        </error-info>
        <error-message>
        Only unit 0 is valid for this encapsulation
        </error-message>
        </rpc-error>
    '''

rpc_xml = '''
    <rpc-error xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:junos="http://xml.juniper.net/junos/12.1X47/junos" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <error-severity>error</error-severity>
    <error-info>
    <bad-element>bgp</bad-element>
    </error-info>
    <error-message>syntax error</error-message>
    </rpc-error>
    '''

conf_xml = '''
    <rpc-error>
        <error-severity>error</error-severity>
        <error-info>
            <bad-element>system1</bad-element>
        </error-info>
        <error-message>syntax error</error-message>
    </rpc-error>
'''


@attr('unit')
class Test_RpcError(unittest.TestCase):

    def test_rpcerror_repr(self):
        rsp = etree.XML(rpc_xml)
        obj = RpcError(rsp=rsp)
        err = 'RpcError(severity: error, bad_element: bgp, message: syntax error)'
        self.assertEquals(str, type(obj.__repr__()))
        self.assertEqual(obj.__repr__(), err)

    def test_rpcerror_jxml_check(self):
        # this test is intended to hit jxml code
        rsp = etree.XML(commit_xml)
        obj = CommitError(rsp=rsp)
        self.assertEqual(obj.rpc_error['bad_element'], 'unit 2')

    def test_ConnectError(self):
        self.dev = Device(host='1.1.1.1', user='rick', password='password123',
                          gather_facts=False)
        obj = ConnectError(self.dev)
        self.assertEqual(obj.user, 'rick')
        self.assertEqual(obj.host, '1.1.1.1')
        self.assertEqual(obj.port, 830)
        self.assertEqual(repr(obj), 'ConnectError(1.1.1.1)')

    def test_CommitError_repr(self):
        rsp = etree.XML(commit_xml)
        obj = CommitError(rsp=rsp)
        err = ("CommitError(edit_path: [edit interfaces ge-0/0/1], "
               "bad_element: unit 2, message: Only unit 0 is valid for this encapsulation)")
        self.assertEqual(obj.__repr__(), err)

    def test_ConfigLoadError_repr(self):
        rsp = etree.XML(conf_xml)
        obj = ConfigLoadError(rsp=rsp)
        err = 'ConfigLoadError(severity: error, bad_element: system1, message: syntax error)'
        self.assertEqual(obj.__repr__(), err)

    def test_RpcTimeoutError_repr(self):
        dev = Device('test')
        obj = RpcTimeoutError(dev=dev, cmd='test', timeout=50)
        err = 'RpcTimeoutError(host: test, cmd: test, timeout: 50)'
        self.assertEqual(obj.__repr__(), err)
