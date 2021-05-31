import json
import requests
from pymongo import MongoClient


class VsApi:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.cookies = None
        self.username_admin = "admin"
        self.passw_admin = "admin"

    def login_admin(self):
        print("start login_admin")
        payload = {}
        url = "http://" + self.ip + ":" + self.port + "/login?username=" + self.username_admin + "&password=" \
              + self.passw_admin
        response = requests.request("POST", url, data=payload)
        self.cookies = response.cookies
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception('Return wrong code')
        print("finish login_admin")

    def create_group(self, group_name):
        print("start create_group")
        payload = {}
        headers = {
            'Content-Type': 'application/json',
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/" + self.username_admin + "/group/" + group_name
        response = requests.request("POST", url, headers=headers, data=payload, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [201, 409]:
            raise Exception('Return wrong code')
        print("finish create_group")

    def get_groups(self):
        print("start get_groups")
        headers = {
            'Content-Type': 'application/json',
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/" + self.username_admin + "/group"
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200]:
            raise Exception('Return wrong code')
        print("finish get_groups")
        return json.loads(response.text)

    def create_tenant(self, tenant_name, password):
        print("start create_tenant")
        payload = {"username": tenant_name,
                   "password": password,
                   "allocatedResources":
                       {"diskStorage": 0,
                        "vCPU": 0,
                        "memoryRAM": 0}
                   }

        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/" + self.username_admin + "/group/" + tenant_name + "/tenant"
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish create_tenant")

    def get_tenants(self):
        print("start get_tenants")
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/" + self.username_admin + "/group"
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish get_tenants")
        return json.loads(response.text)

    def delete_tenant(self, group_name, tenant_id):
        print("start get_tenants")
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/" + self.username_admin + "/group/" + group_name + \
              "/tenant/" + tenant_id
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish get_tenants")
        return json.loads(response.text)

    def purge_vs_instance(self, vsi_id):
        print("start purgeVsInstance")
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/basic/vslcm/vs/" + vsi_id
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish purgeVsInstance")
        return json.loads(response.text)

    def terminate_vs_instance(self, vsi_id):
        print("start terminateVsInstance")
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://" + self.ip + ":" + self.port + "/vs/basic/vslcm/vs/" + vsi_id + "/terminate"
        response = requests.request("POST", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish terminateVsInstance")

    def create_sla(self, group_name, tenant_name):
        print("start create_sla")
        url = "http://" + self.ip + ":" + self.port + "/vs/admin/group/" + group_name + "/tenant/" + \
              tenant_name + "/sla"

        payload = {
            "slaStatus": "ENABLED",
            "slaConstraints": [{
                "maxResourceLimit": {
                    "diskStorage": 120,
                    "vCPU": 10,
                    "memoryRAM": 10240
                },
                "scope": "GLOBAL_VIRTUAL_RESOURCE"
            }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish create_sla")

    def get_sla(self, group_name, tenant_name):
        print("start get_sla")
        url = "http://" + self.ip + ":" + self.port + "/vs/admin/group/" + group_name + "/tenant/" + \
              tenant_name + "/sla"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code in [404]:
            return []
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish get_sla")
        return json.loads(response.text)

    def delete_sla(self, group_name, tenant_name, id_sla):
        print("start delete_sla")
        url = "http://" + self.ip + ":" + self.port + "/vs/admin/group/" + group_name + "/tenant/" + \
              tenant_name + "/sla/" + str(
            id_sla)
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish delete_sla")

    def onboard_nst_vs(self):
        json_file = "json/onboard_nst_vs.json"
        print("start onboard_nst_vs")
        url = "http://" + self.ip + ":" + self.port + "/ns/catalogue/nstemplate"
        with open(json_file, "r") as read_file:
            payload = json.load(read_file)

        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish onboard_nst_vs")

    def get_onboard_nst_vss(self):
        print("start get_onboard_nst_vs")
        url = "http://" + self.ip + ":" + self.port + "/ns/catalogue/nstemplate"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish get_onboard_nst_vs")
        return json.loads(response.text)

    def delete_onboard_nst_vs(self, ns_template_id):
        print("start delete_onboard_nst_vs")
        url = "http://" + self.ip + ":" + self.port + "/ns/catalogue/nstemplate/" + ns_template_id
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish delete_onboard_nst_vs")

    def onboard_vsb_vcdn(self):
        json_file = "json/onboard_vsb_vcdn.json"
        print("start onboard_vsb_vcdn")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsblueprint"
        with open(json_file, "r") as read_file:
            payload = json.load(read_file)

        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish onboard_vsb_vcdn")
        return response.text

    def get_onboard_vsb_vcdns(self):
        print("start onboard_vsb_vcdns")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsblueprint"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish onboard_vsb_vcdns")
        return json.loads(response.text)

    def delete_onboard_vsb_vcdns(self, vs_blueprint_id):
        print("start delete_onboard_vsb_vcdns")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsblueprint/" + vs_blueprint_id
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [204]:
            raise Exception('Return wrong code')
        print("finish delete_onboard_vsb_vcdns")
        return json.dumps(response.text)

    def login_tenant(self, username, password):
        print("start login_tenant")
        url = "http://" + self.ip + ":" + self.port + "/login?username=" + username + "&password=" + password
        payload = None
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        self.cookies = response.cookies
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201, 409]:
            raise Exception('Return wrong code')
        print("finish login_tenant")

    def onboard_vsd_vcdn(self, vs_vsb_id, tenant_id):
        json_file = "json/onboard_vsd_vcdn.json"
        print("start onboard_vsd_vcdn")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsdescriptor"
        with open(json_file, "r") as read_file:
            payload = json.load(read_file)

        payload['tenantId'] = tenant_id
        payload['vsd']['vsBlueprintId'] = vs_vsb_id

        headers = {
            'Content-Type': 'application/json',
        }
        data = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=data, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish onboard_vsd_vcdn")
        return response.text

    def get_onboard_vsd_vcdns(self):
        print("start get_onboard_vsd_vcdns")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsdescriptor"
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish get_onboard_vsd_vcdns")
        return json.loads(response.text)

    def delete_onboard_vsd_vcdn(self, vs_descriptor_id):
        print("start delete_onboard_vsd_vcdn")
        url = "http://" + self.ip + ":" + self.port + "/portal/catalogue/vsdescriptor/" + vs_descriptor_id
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("DELETE", url, headers=headers, cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 204]:
            raise Exception('Return wrong code')
        print("finish delete_onboard_vsd_vcdn")
        return json.dumps(response.text)

    def instantiate_vcdn(self, vs_vsd_id, tenant_id):
        json_file = "json/instantiate_vcdn.json"
        print("start instantiate_vcdn")
        url = "http://" + self.ip + ":" + self.port + "/vs/basic/vslcm/vs"
        with open(json_file, "r") as read_file:
            payload = json.load(read_file)

        payload['vsdId'] = vs_vsd_id
        payload['tenantId'] = tenant_id

        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), cookies=self.cookies)
        print(response.text)
        print("code: " + str(response.status_code))
        if response.status_code not in [200, 201]:
            raise Exception('Return wrong code')
        print("finish instantiate_vcdn")

    def delete_vsb_vsb_sla_objects(self):
        # delete_onboard_vsd_vcdn
        self.login_admin()
        tenants = self.get_tenants()
        for tenant_object in tenants:
            if tenant_object['name'] in ["admin", "user"]:
                continue
            self.login_tenant(tenant_object['name'], tenant_object['name'])
            vsd_vcdns = self.get_onboard_vsd_vcdns()
            for vsd_vcdn in vsd_vcdns:
                vs_descriptor_id = vsd_vcdn['vsDescriptorId']
                self.delete_onboard_vsd_vcdn(vs_descriptor_id)
        # delete_onboard_vsb_vcdns
        self.login_admin()
        vsb_vcdns = self.get_onboard_vsb_vcdns()
        for vsb_vcdn in vsb_vcdns:
            vs_blueprint_id = vsb_vcdn['vsBlueprintId']
            self.delete_onboard_vsb_vcdns(vs_blueprint_id)
        # delete_onboard_nst_vs
        nst_vss = self.get_onboard_nst_vss()
        for nst_vs in nst_vss:
            ns_template_id = nst_vs['nsTemplateId']
            self.delete_onboard_nst_vs(ns_template_id)

        # delete_sla
        tenants = self.get_tenants()
        for tenant_object in tenants:
            if tenant_object['name'] in ["admin", "user"]:
                continue
            else:
                slas = self.get_sla(tenant_object['name'], tenant_object['name'])
                for sla in slas:
                    sla_id = sla["id"]
                    self.delete_sla(tenant_object['name'], tenant_object['name'], sla_id)


def load_nsd_vnfd_to_so(mongodb_ip, mongodb_port):
    db_ip = mongodb_ip
    db_port = mongodb_port
    operation_client = MongoClient(db_ip, int(db_port))
    fgtso_db = operation_client.fgtso
    fgtso_db.nsd.delete_many({})
    fgtso_db.vnfd.delete_many({})
    fgtso_db.ns.delete_many({})
    fgtso_db.nsir.delete_many({})
    fgtso_db.operation.delete_many({})
    fgtso_db.resources.delete_many({})
    fgtso_db.alerts.delete_many({})
    # load desccriptors
    # path to descriptors folders

    path = "json/"
    # list of file names that contain ns and vnf descriptors
    ns_descriptors = ["CDN_all_NSD_0_17.json"]
    vnf_descriptors = ["CDN_PROBE_VNFD_0_9.json",
                       "CDN_SPR1_VNFD_0_9.json", "CDN_SPR2_VNFD_0_9.json",
                       "CDN_WEBSERVER_VNFD_0_9.json"]
    # correspondance of nsdId and nsdCloudifyId
    nsdCloudifyId = {"vCDN_v02": "unknown"}
    # for each nsd create record to be inserted
    nsd_json = {}  # load json file here
    for nsd_file in ns_descriptors:
        with open(path + nsd_file) as nsd_json:
            nsd_json = json.load(nsd_json)
        nsd_record = {"nsdId": nsd_json["nsd"]["nsdIdentifier"],
                      "nsdCloudifyId": nsdCloudifyId[nsd_json["nsd"]["nsdIdentifier"]],
                      "version": nsd_json["nsd"]["version"],
                      "nsdName": nsd_json["nsd"]["nsdName"],
                      "nsdJson": nsd_json,
                      "domain": "local"}
        fgtso_db.nsd.insert_one(nsd_record)
    # for each nsd create record to be inserted
    vnfd_json = {}  # load json file here
    for vnfd_file in vnf_descriptors:
        with open(path + vnfd_file) as vnfd_json:
            vnfd_json = json.load(vnfd_json)
        vnfd_record = {"vnfdId": vnfd_json["vnfdId"],
                       "vnfdVersion": vnfd_json["vnfdVersion"],
                       "vnfdName": vnfd_json["vnfProductName"],
                       "vnfdJson": vnfd_json}
        fgtso_db.vnfd.insert_one(vnfd_record)


if __name__ == "__main__":
    load_nsd_vnfd_to_so("so_mongo", "27017")

    vs_api1 = VsApi("vs_app", "8082")
    # vs_api1.delete_vsb_vsb_sla_objects()

    vs_api1.login_admin()
    group = "CDN"
    vs_api1.create_group(group)
    tenant = "CDN"
    vs_api1.create_tenant(tenant, tenant)
    vs_api1.create_sla(group, tenant)
    vs_api1.onboard_nst_vs()
    vs_vsb_id = vs_api1.onboard_vsb_vcdn()
    tenant = "CDN"
    vs_api1.login_tenant(tenant, tenant)
    vs_vsd_id = vs_api1.onboard_vsd_vcdn(vs_vsb_id, tenant)
    vs_api1.instantiate_vcdn(vs_vsd_id, tenant)

    print("Started instantiate_vcdn")
