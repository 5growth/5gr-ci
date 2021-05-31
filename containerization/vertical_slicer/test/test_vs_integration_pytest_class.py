import pytest
import requests
import re
import json


class TestVSIntegration(object):
    host = 'localhost'
    port = '8082'
    test_group = 'ATOS'
    test_user = 'ATOS'
    test_password = 'ATOS'
    vs_blueprint_id = ''
    vs_descriptor_id = ''
    vs_instance_id = ''
    vs_blueprint = dict()
    http_session = None

    @classmethod
    def setup_class(cls):

        # print("setup_class       class:%s" % cls.__name__)
        cls.http_session = requests.session()


    @classmethod
    def teardown_class(cls):
        # print("teardown_class       class:%s" % cls.__name__)
        cls.http_session.close()

    def test_01login_admin(self):
        url = "http://" + self.host + ":" + self.port + "/login"
        data = {"username": "admin",
                "password": "admin"}

        try:
            res = self.http_session.post(url, data=data)
        except Exception:
            raise ValueError("Exception during connection to " + self.host + ":" + self.port)

        assert res.status_code == 200, 'Can\'t login as admin'

    def test_02group_creating(self):
        url = "http://" + self.host + ":" + self.port + "/vs/admin/group/" + self.test_group
        res = self.http_session.post(url)

        assert res.status_code in [201, 409], "Operation \"Create group\" returned wrong code"
        assert (res.text == '') or (
                'already present in DB' in res.text), "Operation \"Create group\" returned wrong message"

    def test_03tenant_creating(self):
        url = "http://" + self.host + ":" + self.port + "/vs/admin/group/" + self.test_group + "/tenant"
        data = {"username": self.test_user,
                "password": self.test_password}
        headers = {"Content-Type": "application/json",
                   "Accept": "*/*"}
        res = self.http_session.post(url, data=json.dumps(data), headers=headers)

        assert res.status_code in [201, 409], "Operation \"Create tenant\" returned wrong code"
        assert (res.text == '') or (
                'already present in DB' in res.text), "Operation \"Create tenant\" returned wrong message"

    def test_04tenant_sla_creating(self):
        url = "http://" + self.host + ":" + self.port + "/vs/admin/group/" + self.test_group + "/tenant/" + self.test_user + "/sla"
        headers = {"Content-Type": "application/json",
                   "Accept": "*/*"}
        data = {
            "slaStatus": "ENABLED",
            "slaConstraints": [{
                "maxResourceLimit": {
                    "diskStorage": 100,
                    "vCPU": 4,
                    "memoryRAM": 8192
                },
                "scope": "GLOBAL_VIRTUAL_RESOURCE"
            }
            ]
        }
        res = self.http_session.post(url, data=json.dumps(data), headers=headers)

        assert res.status_code in [201], "Operation \"Create tenant Sla\" returned wrong code"
        assert re.match(r'\d+', res.text), "Operation \"Create tenant Sla\" returned wrong message"

    def test_05vs_blueprint_creating(self):
        url = "http://" + self.host + ":" + self.port + "/vs/catalogue/vsblueprint"
        self.vs_blueprint = {
            "vsBlueprint": {
                "version": "0.1",
                "name": "CDN",
                "description": "Content Delivery Network",
                "parameters": [{
                    "parameterId": "users",
                    "parameterName": "users",
                    "parameterType": "number",
                    "parameterDescription": "number of CDN users",
                    "applicabilityField": "media"
                }]
            },
            "translationRules": [{
                "nsdId": "vCDN_v02",
                "nsdVersion": "0.2",
                "nsFlavourId": "df_vCDN",
                "nsInstantiationLevelId": "il_vCDN_big",
                "input": [{
                    "parameterId": "users",
                    "minValue": 1001,
                    "maxValue": 2500
                }]
            }, {
                "nsdId": "vCDN_v02",
                "nsdVersion": "0.2",
                "nsFlavourId": "df_vCDN",
                "nsInstantiationLevelId": "il_vCDN_small",
                "input": [{
                    "parameterId": "users",
                    "minValue": 1,
                    "maxValue": 1000
                }]
            }]
        }
        headers = {"Content-Type": "application/json",
                   "Accept": "*/*"}
        res = self.http_session.post(url, data=json.dumps(self.vs_blueprint), headers=headers)
        assert res.status_code in [201, 409], "Operation \"Create VS blueprint\" returned wrong code"
        assert re.match(r'\d+', res.text) or (
                'already present in DB' in res.text), "Operation \"Create VS blueprint\" returned wrong message"

        if 'already present in DB' in res.text:
            url = "http://" + self.host + ":" + self.port + "/vs/catalogue/vsblueprint"
            res = self.http_session.get(url, data=json.dumps(self.vs_blueprint), headers=headers)
            for vs_blueprint in json.loads(res.text):
                if (vs_blueprint['vsBlueprintVersion'] == self.vs_blueprint['vsBlueprint']['version']) and (
                        vs_blueprint['name'] == self.vs_blueprint['vsBlueprint']['name']):
                    TestVSIntegration.vs_blueprint_id = vs_blueprint['vsBlueprintId']

        else:
            TestVSIntegration.vs_blueprint_id = res.text

    def test_06login_test_user(self):
        url = "http://" + self.host + ":" + self.port + "/login"
        data = {"username": self.test_user,
                "password": self.test_password}

        res = self.http_session.post(url, data=data)
        assert res.status_code == 200, "Couldn\'t login as " + self.test_user

    def test_07vs_descriptor_creating(self):

        url = "http://" + self.host + ":" + self.port + "/vs/catalogue/vsdescriptor"
        data = \
            {
                "vsd": {
                    "name": "VSD_CDN_small_new",
                    "version": "0.1",
                    "vsBlueprintId": self.vs_blueprint_id,
                    "sst": "EMBB",
                    "managementType": "PROVIDER_MANAGED",
                    "qosParameters": {
                        "users": "1000"
                    }
                },
                "tenantId": self.test_user,
                "isPublic": 'true'
            }

        headers = {"Content-Type": "application/json",
                   "Accept": "*/*"}

        res = self.http_session.post(url, data=json.dumps(data), headers=headers)
        assert res.status_code in [201, 409], "Operation \"Create VS descriptor\" returned wrong code"
        assert re.match(r'\d+', res.text) or (
                'already present' in res.text), "Operation \"Create VS descriptor\" returned wrong message"

        if 'already present' in res.text:
            url = "http://" + self.host + ":" + self.port + "/vs/catalogue/vsdescriptor"
            res = self.http_session.get(url, data=json.dumps(self.vs_blueprint), headers=headers)
            for vs_descriptor in json.loads(res.text):
                if (vs_descriptor['vsBlueprintId'] == self.vs_blueprint_id):
                    TestVSIntegration.vs_descriptor_id = vs_descriptor['vsDescriptorId']
                    break
        else:
            TestVSIntegration.vs_descriptor_id = res.text

    def test_08vs_instantiate(self):
        url = "http://" + self.host + ":" + self.port + "/vs/basic/vslcm/vs"
        data = \
            {
                "name": "CDN_small",
                "description": "CDN service for max 1000 users",
                "vsdId": self.vs_descriptor_id,
                "tenantId": self.test_user
            }

        headers = {"Content-Type": "application/json",
                   "Accept": "*/*"}

        res = self.http_session.post(url, data=json.dumps(data), headers=headers)
        assert res.status_code in [201], "Operation \"Create VS descriptor\" returned wrong code"
        assert re.match(r'\d+', res.text), "Operation \"Create VS descriptor\" returned wrong message"
        TestVSIntegration.vs_instance_id = res.text

    def test_09check_status(self):
        is_continue = True
        while is_continue > 0:
            url = "http://" + self.host + ":" + self.port + "/vs/basic/vslcm/vs/" + self.vs_instance_id
            res = self.http_session.get(url)
            try:
                vs_instance = json.loads(res.text)
            except ValueError:
                is_continue = False
            else:
                if vs_instance['status'] == 'FAILED':
                    raise ValueError(vs_instance['errorMessage'])
