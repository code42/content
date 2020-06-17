import json
import pytest
from requests import Response
from py42.sdk import SDKClient
from py42.response import Py42Response
from Code42 import (
    Code42Client,
    build_query_payload,
    map_observation_to_security_query,
    map_to_code42_event_context,
    map_to_code42_alert_context,
    map_to_file_context,
    alert_get_command,
    alert_resolve_command,
    departingemployee_add_command,
    departingemployee_remove_command,
    departingemployee_get_all_command,
    highriskemployee_add_command,
    highriskemployee_remove_command,
    highriskemployee_get_all_command,
    highriskemployee_add_risk_tags_command,
    highriskemployee_remove_risk_tags_command,
    fetch_incidents,
    securitydata_search_command,
)
import time

MOCK_URL = "https://123-fake-api.com"

MOCK_AUTH = ("123", "123")

MOCK_FETCH_TIME = "24 hours"

MOCK_SECURITY_DATA_SEARCH_QUERY = {
    "hash": "d41d8cd98f00b204e9800998ecf8427e",
    "hostname": "DESKTOP-0001",
    "username": "user3@example.com",
    "exposure": "ApplicationRead",
    "results": 50,
}

MOCK_SECURITY_EVENT_RESPONSE = """
{
    "totalCount":3,
    "fileEvents":[
        {
            "eventId":"0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType":"READ_BY_APP",
            "eventTimestamp":"2020-05-28T12:46:39.838Z",
            "insertionTimestamp":"2020-05-28T12:51:50.040Z",
            "fieldErrors":[],
            "filePath":"C:/Users/QA/Downloads/",
            "fileName":"company_secrets.txt",
            "fileType":"FILE",
            "fileCategory":"IMAGE",
            "fileCategoryByBytes":"Image",
            "fileCategoryByExtension":"Image",
            "fileSize":265122,
            "fileOwner":"Test",
            "md5Checksum":"9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum":"34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp":"2020-05-28T12:43:34.902Z",
            "modifyTimestamp":"2020-05-28T12:43:35.105Z",
            "deviceUserName":"test@example.com",
            "osHostName":"HOSTNAME",
            "domainName":"host.docker.internal",
            "publicIpAddress":"162.222.47.183",
            "privateIpAddresses":["172.20.128.36","127.0.0.1"],
            "deviceUid":"935873453596901068",
            "userUid":"912098363086307495",
            "actor":null,
            "directoryId":[],
            "source":"Endpoint",
            "url":null,
            "shared":null,
            "sharedWith":[],
            "sharingTypeAdded":[],
            "cloudDriveId":null,
            "detectionSourceAlias":null,
            "fileId":null,
            "exposure":["ApplicationRead"],
            "processOwner":"QA",
            "processName":"chrome.exe",
            "windowTitle":["Jira"],
            "tabUrl":"example.com",
            "removableMediaVendor":null,
            "removableMediaName":null,
            "removableMediaSerialNumber":null,
            "removableMediaCapacity":null,
            "removableMediaBusType":null,
            "removableMediaMediaName":null,
            "removableMediaVolumeName":[],
            "removableMediaPartitionId":[],
            "syncDestination":null,
            "emailDlpPolicyNames":null,
            "emailSubject":null,
            "emailSender":null,
            "emailFrom":null,
            "emailRecipients":null,
            "outsideActiveHours":false,
            "mimeTypeByBytes":"image/png",
            "mimeTypeByExtension":"image/png",
            "mimeTypeMismatch":false,
            "printJobName":null,
            "printerName":null,
            "printedFilesBackupPath":null,
            "remoteActivity":"UNKNOWN",
            "trusted":false
        },
        {
            "eventId":"0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType":"READ_BY_APP",
            "eventTimestamp":"2020-05-28T12:46:39.838Z",
            "insertionTimestamp":"2020-05-28T12:51:50.040Z",
            "fieldErrors":[],
            "filePath":"C:/Users/QA/Downloads/",
            "fileName":"data.jpg",
            "fileType":"FILE",
            "fileCategory":"IMAGE",
            "fileCategoryByBytes":"Image",
            "fileCategoryByExtension":"Image",
            "fileSize":265122,
            "fileOwner":"QA",
            "md5Checksum":"9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum":"34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp":"2020-05-28T12:43:34.902Z",
            "modifyTimestamp":"2020-05-28T12:43:35.105Z",
            "deviceUserName":"test@example.com",
            "osHostName":"TEST'S MAC",
            "domainName":"host.docker.internal",
            "publicIpAddress":"162.222.47.183",
            "privateIpAddresses":["127.0.0.1"],
            "deviceUid":"935873453596901068",
            "userUid":"912098363086307495",
            "actor":null,
            "directoryId":[],
            "source":"Endpoint",
            "url":null,
            "shared":null,
            "sharedWith":[],
            "sharingTypeAdded":[],
            "cloudDriveId":null,
            "detectionSourceAlias":null,
            "fileId":null,
            "exposure":["ApplicationRead"],
            "processOwner":"QA",
            "processName":"chrome.exe",
            "windowTitle":["Jira"],
            "tabUrl":"example.com/test",
            "removableMediaVendor":null,
            "removableMediaName":null,
            "removableMediaSerialNumber":null,
            "removableMediaCapacity":null,
            "removableMediaBusType":null,
            "removableMediaMediaName":null,
            "removableMediaVolumeName":[],
            "removableMediaPartitionId":[],
            "syncDestination":null,
            "emailDlpPolicyNames":null,
            "emailSubject":null,
            "emailSender":null,
            "emailFrom":null,
            "emailRecipients":null,
            "outsideActiveHours":false,
            "mimeTypeByBytes":"image/png",
            "mimeTypeByExtension":"image/png",
            "mimeTypeMismatch":false,
            "printJobName":null,
            "printerName":null,
            "printedFilesBackupPath":null,
            "remoteActivity":"UNKNOWN",
            "trusted":false
        },
        {
            "eventId":"0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
            "eventType":"READ_BY_APP",
            "eventTimestamp":"2020-05-28T12:46:39.838Z",
            "insertionTimestamp":"2020-05-28T12:51:50.040Z",
            "fieldErrors":[],
            "filePath":"C:/Users/QA/Downloads/",
            "fileName":"confidential.pdf",
            "fileType":"FILE",
            "fileCategory":"IMAGE",
            "fileCategoryByBytes":"Image",
            "fileCategoryByExtension":"Image",
            "fileSize":265122,
            "fileOwner":"Mock",
            "md5Checksum":"9cea266b4e07974df1982ae3b9de92ce",
            "sha256Checksum":"34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
            "createTimestamp":"2020-05-28T12:43:34.902Z",
            "modifyTimestamp":"2020-05-28T12:43:35.105Z",
            "deviceUserName":"test@example.com",
            "osHostName":"Test's Windows",
            "domainName":"host.docker.internal",
            "publicIpAddress":"162.222.47.183",
            "privateIpAddresses":["0:0:0:0:0:0:0:1","127.0.0.1"],
            "deviceUid":"935873453596901068",
            "userUid":"912098363086307495",
            "actor":null,
            "directoryId":[],
            "source":"Endpoint",
            "url":null,
            "shared":null,
            "sharedWith":[],
            "sharingTypeAdded":[],
            "cloudDriveId":null,
            "detectionSourceAlias":null,
            "fileId":null,
            "exposure":["ApplicationRead"],
            "processOwner":"QA",
            "processName":"chrome.exe",
            "windowTitle":["Jira"],
            "tabUrl":"example.com/foo",
            "removableMediaVendor":null,
            "removableMediaName":null,
            "removableMediaSerialNumber":null,
            "removableMediaCapacity":null,
            "removableMediaBusType":null,
            "removableMediaMediaName":null,
            "removableMediaVolumeName":[],
            "removableMediaPartitionId":[],
            "syncDestination":null,
            "emailDlpPolicyNames":null,
            "emailSubject":null,
            "emailSender":null,
            "emailFrom":null,
            "emailRecipients":null,
            "outsideActiveHours":false,
            "mimeTypeByBytes":"image/png",
            "mimeTypeByExtension":"image/png",
            "mimeTypeMismatch":false,
            "printJobName":null,
            "printerName":null,
            "printedFilesBackupPath":null,
            "remoteActivity":"UNKNOWN",
            "trusted":false
        }
    ]
}
"""

MOCK_CODE42_EVENT_CONTEXT = [
    {
        "ApplicationTabURL": "example.com",
        "DevicePrivateIPAddress": ["172.20.128.36", "127.0.0.1"],
        "DeviceUsername": "test@example.com",
        "EndpointID": "935873453596901068",
        "EventID": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "EventTimestamp": "2020-05-28T12:46:39.838Z",
        "EventType": "READ_BY_APP",
        "Exposure": ["ApplicationRead"],
        "FileCategory": "IMAGE",
        "FileCreated": "2020-05-28T12:43:34.902Z",
        "FileHostname": "HOSTNAME",
        "FileMD5": "9cea266b4e07974df1982ae3b9de92ce",
        "FileModified": "2020-05-28T12:43:35.105Z",
        "FileName": "company_secrets.txt",
        "FileOwner": "Test",
        "FilePath": "C:/Users/QA/Downloads/",
        "FileSHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "FileSize": 265122,
        "ProcessName": "chrome.exe",
        "ProcessOwner": "QA",
        "Source": "Endpoint",
        "WindowTitle": ["Jira"],
    },
    {
        "ApplicationTabURL": "example.com/test",
        "DevicePrivateIPAddress": ["127.0.0.1"],
        "DeviceUsername": "test@example.com",
        "EndpointID": "935873453596901068",
        "EventID": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "EventTimestamp": "2020-05-28T12:46:39.838Z",
        "EventType": "READ_BY_APP",
        "Exposure": ["ApplicationRead"],
        "FileCategory": "IMAGE",
        "FileCreated": "2020-05-28T12:43:34.902Z",
        "FileHostname": "TEST'S MAC",
        "FileMD5": "9cea266b4e07974df1982ae3b9de92ce",
        "FileModified": "2020-05-28T12:43:35.105Z",
        "FileName": "data.jpg",
        "FileOwner": "QA",
        "FilePath": "C:/Users/QA/Downloads/",
        "FileSHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "FileSize": 265122,
        "ProcessName": "chrome.exe",
        "ProcessOwner": "QA",
        "Source": "Endpoint",
        "WindowTitle": ["Jira"],
    },
    {
        "ApplicationTabURL": "example.com/foo",
        "DevicePrivateIPAddress": ["0:0:0:0:0:0:0:1", "127.0.0.1"],
        "DeviceUsername": "test@example.com",
        "EndpointID": "935873453596901068",
        "EventID": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
        "EventTimestamp": "2020-05-28T12:46:39.838Z",
        "EventType": "READ_BY_APP",
        "Exposure": ["ApplicationRead"],
        "FileCategory": "IMAGE",
        "FileCreated": "2020-05-28T12:43:34.902Z",
        "FileHostname": "Test's Windows",
        "FileMD5": "9cea266b4e07974df1982ae3b9de92ce",
        "FileModified": "2020-05-28T12:43:35.105Z",
        "FileName": "confidential.pdf",
        "FileOwner": "Mock",
        "FilePath": "C:/Users/QA/Downloads/",
        "FileSHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "FileSize": 265122,
        "ProcessName": "chrome.exe",
        "ProcessOwner": "QA",
        "Source": "Endpoint",
        "WindowTitle": ["Jira"],
    },
]

MOCK_FILE_CONTEXT = [
    {
        "Hostname": "HOSTNAME",
        "MD5": "9cea266b4e07974df1982ae3b9de92ce",
        "Name": "company_secrets.txt",
        "Path": "C:/Users/QA/Downloads/",
        "SHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "Size": 265122,
    },
    {
        "Hostname": "TEST'S MAC",
        "MD5": "9cea266b4e07974df1982ae3b9de92ce",
        "Name": "data.jpg",
        "Path": "C:/Users/QA/Downloads/",
        "SHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "Size": 265122,
    },
    {
        "Hostname": "Test's Windows",
        "MD5": "9cea266b4e07974df1982ae3b9de92ce",
        "Name": "confidential.pdf",
        "Path": "C:/Users/QA/Downloads/",
        "SHA256": "34d0c9fc9c907ec374cf7e8ca1ff8a172e36eccee687f0a9b69dd169debb81e1",
        "Size": 265122,
    },
]

MOCK_ALERTS_RESPONSE = """{
  "type$": "ALERT_QUERY_RESPONSE",
  "alerts": [
    {
      "type$": "ALERT_SUMMARY",
      "tenantId": "1d700000-af5b-4231-9d8e-df6434d00000",
      "type": "FED_ENDPOINT_EXFILTRATION",
      "name": "Exposure on an endpoint",
      "description": "This default rule alerts you when departing employees move data from an endpoint.",
      "actor": "test.testerson@example.com",
      "target": "N/A",
      "severity": "HIGH",
      "ruleId": "9befe477-3487-40b7-89a6-bbcced4cf1fe",
      "ruleSource": "Departing Employee",
      "id": "fbeaabc1-9205-4620-ad53-95d0633429a3",
      "createdAt": "2020-05-04T20:46:45.8106280Z",
      "state": "OPEN"
    },
    {
      "type$": "ALERT_SUMMARY",
      "tenantId": "1d700000-af5b-4231-9d8e-df6434d00000",
      "type": "FED_ENDPOINT_EXFILTRATION",
      "name": "Exposure on an endpoint",
      "description": "This default rule alerts you when departing employees move data from an endpoint.",
      "actor": "test.testerson@example.com",
      "target": "N/A",
      "severity": "LOW",
      "ruleId": "9befe477-3487-40b7-89a6-bbcced4cf1fe",
      "ruleSource": "Departing Employee",
      "id": "6bb7ca1e-c8cf-447d-a732-9652869e42d0",
      "createdAt": "2020-05-04T20:35:54.2400240Z",
      "state": "OPEN"
    },
    {
      "type$": "ALERT_SUMMARY",
      "tenantId": "1d700000-af5b-4231-9d8e-df6434d00000",
      "type": "FED_ENDPOINT_EXFILTRATION",
      "name": "Exposure on an endpoint",
      "description": "This default rule alerts you when departing employees move data from an endpoint.",
      "actor": "test.testerson@example.com",
      "target": "N/A",
      "severity": "HIGH",
      "ruleId": "9befe477-3487-40b7-89a6-bbcced4cf1fe",
      "ruleSource": "Departing Employee",
      "id": "c2c3aef3-8fd9-4e7a-a04e-16bec9e27625",
      "createdAt": "2020-05-04T20:19:34.7121300Z",
      "state": "OPEN"
    }
  ],
  "totalCount": 3,
  "problems": []
}"""

MOCK_ALERT_DETAILS_RESPONSE = """{
    "type$": "ALERT_DETAILS_RESPONSE",
    "alerts": [
        {"type$": "ALERT_DETAILS",
        "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
        "type": "FED_ENDPOINT_EXFILTRATION",
        "name": "Departing Employee Alert",
        "description": "Cortex XSOAR is cool.",
        "actor": "user1@example.com",
        "actorId": "912098363086307495",
        "target": "N/A",
        "severity": "HIGH",
        "ruleId": "4576576e-13cb-4f88-be3a-ee77739de649",
        "ruleSource": "Alerting",
        "id": "36fb8ca5-0533-4d25-9763-e09d35d60610",
        "createdAt": "2019-10-02T17:02:23.5867670Z",
        "state": "OPEN",
        "observations": [
            {
                "type$": "OBSERVATION",
                "id": "240526fc-3a32-4755-85ab-c6ee6e7f31ce",
                "observedAt": "2020-05-28T12:50:00.0000000Z",
                "type": "FedEndpointExfiltration",
                "data": {
                    "type$": "OBSERVED_ENDPOINT_ACTIVITY",
                    "id": "240526fc-3a32-4755-85ab-c6ee6e7f31ce",
                    "sources": ["Endpoint"],
                    "exposureTypes": ["ApplicationRead"],
                    "firstActivityAt": "2020-05-28T12:50:00.0000000Z",
                    "lastActivityAt": "2020-05-28T12:50:00.0000000Z",
                    "fileCount": 3,
                    "totalFileSize": 533846,
                    "fileCategories": [
                        {
                            "type$": "OBSERVED_FILE_CATEGORY",
                            "category": "Image",
                            "fileCount": 3,
                            "totalFileSize": 533846,
                            "isSignificant": true
                        }
                    ],
                    "files": [
                        {
                            "type$": "OBSERVED_FILE",
                            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_5",
                            "path": "C:/Users/QA/Downloads/",
                            "name": "Customers.jpg",
                            "category": "Image",
                            "size": 265122
                        },
                        {
                            "type$": "OBSERVED_FILE",
                            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_6",
                            "path": "C:/Users/QA/Downloads/",
                            "name": "data.png",
                            "category": "Image",
                            "size": 129129
                        },
                        {
                            "type$": "OBSERVED_FILE",
                            "eventId": "0_1d71796f-af5b-4231-9d8e-df6434da4663_935873453596901068_956171635867906205_7",
                            "path": "C:/Users/QA/Downloads/",
                            "name": "company_secrets.ps",
                            "category": "Image",
                            "size": 139595
                        }
                    ],
                    "syncToServices": [],
                    "sendingIpAddresses": ["127.0.0.1"]
                    }
                }
            ]
        }
    ]
}"""

MOCK_CODE42_ALERT_CONTEXT = [
    {
        "ID": "36fb8ca5-0533-4d25-9763-e09d35d60610",
        "Name": "Departing Employee Alert",
        "Description": "Cortex XSOAR is cool.",
        "Occurred": "2019-10-02T17:02:23.5867670Z",
        "Severity": "HIGH",
        "State": "OPEN",
        "Type": "FED_ENDPOINT_EXFILTRATION",
        "Username": "user1@example.com",
    },
    {
        "ID": "18ac641d-7d9c-4d37-a48f-c89396c07d03",
        "Name": "High-Risk Employee Alert",
        "Occurred": "2019-10-02T17:02:24.2071980Z",
        "Severity": "MEDIUM",
        "State": "OPEN",
        "Type": "FED_CLOUD_SHARE_PERMISSIONS",
        "Username": "user2@example.com",
    },
    {
        "ID": "3137ff1b-b824-42e4-a476-22bccdd8ddb8",
        "Name": "Custom Alert 1",
        "Occurred": "2019-10-02T17:03:28.2885720Z",
        "Severity": "LOW",
        "State": "OPEN",
        "Type": "FED_ENDPOINT_EXFILTRATION",
        "Username": "user3@example.com",
    },
]

MOCK_FILE_EVENT_QUERY_PAYLOAD = {
    "groupClause": "AND",
    "groups": [
        {
            "filterClause": "AND",
            "filters": [
                {
                    "operator": "IS",
                    "term": "md5Checksum",
                    "value": "d41d8cd98f00b204e9800998ecf8427e",
                }
            ],
        },
        {
            "filterClause": "AND",
            "filters": [{"operator": "IS", "term": "osHostName", "value": "DESKTOP-0001"}],
        },
        {
            "filterClause": "AND",
            "filters": [{"operator": "IS", "term": "deviceUserName", "value": "user3@example.com"}],
        },
        {
            "filterClause": "AND",
            "filters": [{"operator": "IS", "term": "exposure", "value": "ApplicationRead"}],
        },
    ],
    "pgNum": 1,
    "pgSize": 50,
    "srtDir": "asc",
    "srtKey": "eventId",
}

MOCK_OBSERVATION_QUERIES = [
    {
        "groupClause": "AND",
        "groups": [
            {
                "filterClause": "AND",
                "filters": [
                    {"operator": "IS", "term": "deviceUserName", "value": "user1@example.com"}
                ],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_AFTER",
                        "term": "eventTimestamp",
                        "value": "2020-05-28T12:50:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_BEFORE",
                        "term": "eventTimestamp",
                        "value": "2020-05-28T12:50:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "OR",
                "filters": [
                    {"operator": "IS", "term": "eventType", "value": "CREATED"},
                    {"operator": "IS", "term": "eventType", "value": "MODIFIED"},
                    {"operator": "IS", "term": "eventType", "value": "READ_BY_APP"},
                ],
            },
            {
                "filterClause": "AND",
                "filters": [{"operator": "IS", "term": "exposure", "value": "ApplicationRead"}],
            },
            {
                "filterClause": "AND",
                "filters": [{"operator": "IS", "term": "fileCategory", "value": "IMAGE"}],
            },
        ],
        "pgNum": 1,
        "pgSize": 10000,
        "srtDir": "asc",
        "srtKey": "eventId",
    },
    {
        "groupClause": "AND",
        "groups": [
            {
                "filterClause": "AND",
                "filters": [{"operator": "IS", "term": "actor", "value": "user2@example.com"}],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_AFTER",
                        "term": "eventTimestamp",
                        "value": "2019-10-02T16:50:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_BEFORE",
                        "term": "eventTimestamp",
                        "value": "2019-10-02T16:55:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "OR",
                "filters": [
                    {"operator": "IS", "term": "exposure", "value": "IsPublic"},
                    {"operator": "IS", "term": "exposure", "value": "SharedViaLink"},
                ],
            },
        ],
        "pgNum": 1,
        "pgSize": 10000,
        "srtDir": "asc",
        "srtKey": "eventId",
    },
    {
        "groupClause": "AND",
        "groups": [
            {
                "filterClause": "AND",
                "filters": [
                    {"operator": "IS", "term": "deviceUserName", "value": "user3@example.com"}
                ],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_AFTER",
                        "term": "eventTimestamp",
                        "value": "2019-10-02T16:50:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "AND",
                "filters": [
                    {
                        "operator": "ON_OR_BEFORE",
                        "term": "eventTimestamp",
                        "value": "2019-10-02T16:50:00.000Z",
                    }
                ],
            },
            {
                "filterClause": "OR",
                "filters": [
                    {"operator": "IS", "term": "eventType", "value": "CREATED"},
                    {"operator": "IS", "term": "eventType", "value": "MODIFIED"},
                    {"operator": "IS", "term": "eventType", "value": "READ_BY_APP"},
                ],
            },
            {
                "filterClause": "AND",
                "filters": [{"operator": "IS", "term": "exposure", "value": "RemovableMedia"}],
            },
        ],
        "pgNum": 1,
        "pgSize": 10000,
        "srtDir": "asc",
        "srtKey": "eventId",
    },
]


MOCK_GET_USER_RESPONSE = """
{
    "totalCount": 1,
    "users": [
        {
            "userId": 123456,
            "userUid": "123412341234123412",
            "status": "Active",
            "username": "test.testerson@example.com",
            "email": "test.testerson@example.com",
            "firstName": "Test",
            "lastName": "Testerson",
            "quotaInBytes": -1,
            "orgId": 1111,
            "orgUid": "81111247111106706",
            "orgName": "Testers",
            "userExtRef": null,
            "notes": null,
            "active": true,
            "blocked": false,
            "emailPromo": true,
            "invited": false,
            "orgType": "ENTERPRISE",
            "usernameIsAnEmail": true,
            "creationDate": "2019-09-30T21:03:08.587Z",
            "modificationDate": "2020-04-10T11:49:49.987Z",
            "passwordReset": false,
            "localAuthenticationOnly": false,
            "licenses": ["admin.securityTools"]
        }
    ]
}"""

MOCK_GET_ALL_DEPARTING_EMPLOYEES_RESPONSE = """
{
    "items": [
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": 1000,
            "userId": "890973079883949999",
            "userName": "test@example.com",
            "displayName": "Name",
            "notes": "",
            "createdAt": "2019-10-25T13:31:14.1199010Z",
            "status": "OPEN",
            "cloudUsernames": ["test@cloud.com"],
            "totalBytes": 139856482,
            "numEvents": 11
        },
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": 1000,
            "userId": "123412341234123412",
            "userName": "user1@example.com",
            "displayName": "Name",
            "notes": "",
            "createdAt": "2019-10-25T13:31:14.1199010Z",
            "status": "OPEN",
            "cloudUsernames": ["test@example.com"],
            "totalBytes": 139856482,
            "numEvents": 11
        },
        {
            "type$": "DEPARTING_EMPLOYEE_V2",
            "tenantId": 1000,
            "userId": "890973079883949999",
            "userName": "test@example.com",
            "displayName": "Name",
            "notes": "",
            "createdAt": "2019-10-25T13:31:14.1199010Z",
            "status": "OPEN",
            "cloudUsernames": ["test@example.com"],
            "totalBytes": 139856482,
            "numEvents": 11
        }
    ],
    "totalCount": 3
}
"""

MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE = """
{
  "type$": "HIGH_RISK_SEARCH_RESPONSE_V2",
  "items": [
    {
      "type$": "HIGH_RISK_EMPLOYEE_V2",
      "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
      "userId": "91209844444444444",
      "userName": "karen@example.com",
      "displayName": "Karen",
      "notes": "High risk notes",
      "createdAt": "2020-05-22T17:47:42.7054310Z",
      "status": "OPEN",
      "cloudUsernames": [
        "karen+test@example.com",
        "karen+manager@example.com"
      ],
      "totalBytes": 816122,
      "numEvents": 13,
      "riskFactors": [
        "PERFORMANCE_CONCERNS",
        "SUSPICIOUS_SYSTEM_ACTIVITY",
        "POOR_SECURITY_PRACTICES"
      ]
    },
    {
      "type$": "HIGH_RISK_EMPLOYEE_V2",
      "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
      "userId": "94222222975202822222",
      "userName": "james.test@example.com",
      "displayName": "James Test",
      "notes": "tests and more tests",
      "createdAt": "2020-05-28T12:39:57.2058370Z",
      "status": "OPEN",
      "cloudUsernames": [
        "james.test+test@example.com"
      ]
    },
    {
      "type$": "HIGH_RISK_EMPLOYEE_V2",
      "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
      "userId": "123412341234123412",
      "userName": "user1@example.com",
      "displayName": "User 1",
      "notes": "Test Notes",
      "createdAt": "2020-05-22T17:47:42.4836920Z",
      "status": "OPEN",
      "cloudUsernames": [
        "test@example.com",
        "abc123@example.com"
      ],
      "riskFactors": [
        "PERFORMANCE_CONCERNS"
      ]
    }
  ],
  "totalCount": 3,
  "rollups": [
    {
      "type$": "HIGH_RISK_FILTER_ROLLUP_V2",
      "filterType": "OPEN",
      "totalCount": 3
    },
    {
      "type$": "HIGH_RISK_FILTER_ROLLUP_V2",
      "filterType": "EXFILTRATION_24_HOURS",
      "totalCount": 0
    },
    {
      "type$": "HIGH_RISK_FILTER_ROLLUP_V2",
      "filterType": "EXFILTRATION_30_DAYS",
      "totalCount": 1
    }
  ],
  "filterType": "OPEN",
  "pgSize": 10,
  "pgNum": 1,
  "srtKey": "NUM_EVENTS",
  "srtDirection": "DESC"
}
"""


@pytest.fixture
def code42_sdk_mock(mocker):
    c42_sdk_mock = mocker.MagicMock(spec=SDKClient)

    # Setup mock alert details
    alert_details_response = create_mock_code42_sdk_response(mocker, MOCK_ALERT_DETAILS_RESPONSE)
    c42_sdk_mock.alerts.get_details.return_value = alert_details_response

    # Setup alerts for querying
    alerts_response = create_mock_code42_sdk_response(mocker, MOCK_ALERTS_RESPONSE)
    c42_sdk_mock.alerts.search.return_value = alerts_response

    # Setup mock user
    get_user_response = create_mock_code42_sdk_response(mocker, MOCK_GET_USER_RESPONSE)
    c42_sdk_mock.users.get_by_username.return_value = get_user_response

    # Setup file events
    search_file_events_response = create_mock_code42_sdk_response(
        mocker, MOCK_SECURITY_EVENT_RESPONSE
    )
    c42_sdk_mock.securitydata.search_file_events.return_value = search_file_events_response

    # Setup get all departing employees
    all_departing_employees_response = create_mock_code42_sdk_response_generator(
        mocker, [MOCK_GET_ALL_DEPARTING_EMPLOYEES_RESPONSE]
    )
    c42_sdk_mock.detectionlists.departing_employee.get_all.return_value = (
        all_departing_employees_response
    )

    # Setup get all high risk employees
    all_high_risk_employees_response = create_mock_code42_sdk_response_generator(
        mocker, [MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE]
    )
    c42_sdk_mock.detectionlists.high_risk_employee.get_all.return_value = (
        all_high_risk_employees_response
    )

    return c42_sdk_mock


def create_mock_code42_sdk_response(mocker, response_text):
    response_mock = mocker.MagicMock(spec=Response)
    response_mock.text = response_text
    return Py42Response(response_mock)


def create_mock_code42_sdk_response_generator(mocker, response_pages):
    return (create_mock_code42_sdk_response(mocker, page) for page in response_pages)


def create_client(sdk):
    return Code42Client(sdk=sdk, base_url=MOCK_URL, auth=MOCK_AUTH, verify=False, proxy=None)


"""TESTS"""


def test_build_query_payload():
    query = build_query_payload(MOCK_SECURITY_DATA_SEARCH_QUERY)
    assert query.sort_key == MOCK_FILE_EVENT_QUERY_PAYLOAD["srtKey"]
    assert query.page_number == MOCK_FILE_EVENT_QUERY_PAYLOAD["pgNum"]
    assert json.loads((str(query))) == MOCK_FILE_EVENT_QUERY_PAYLOAD


def test_map_observation_to_security_query():
    response = json.loads(MOCK_ALERT_DETAILS_RESPONSE)
    alerts = response["alerts"]
    for i in range(0, len(alerts)):
        observation = alerts[i]["observations"][0]
        actor = alerts[i]["actor"]
        query = map_observation_to_security_query(observation, actor)
        assert query.sort_key == MOCK_OBSERVATION_QUERIES[i]["srtKey"]
        assert query.page_number == MOCK_OBSERVATION_QUERIES[i]["pgNum"]
        assert json.loads(str(query)) == MOCK_OBSERVATION_QUERIES[i]


def test_map_to_code42_event_context():
    response = json.loads(MOCK_SECURITY_EVENT_RESPONSE)
    file_events = response["fileEvents"]
    for i in range(0, len(file_events)):
        context = map_to_code42_event_context(file_events[i])
        assert context == MOCK_CODE42_EVENT_CONTEXT[i]


def test_map_to_code42_alert_context():
    response = json.loads(MOCK_ALERT_DETAILS_RESPONSE)
    alerts = response["alerts"]
    for i in range(0, len(alerts)):
        context = map_to_code42_alert_context(alerts[i])
        assert context == MOCK_CODE42_ALERT_CONTEXT[i]


def test_map_to_file_context():
    response = json.loads(MOCK_SECURITY_EVENT_RESPONSE)
    file_events = response["fileEvents"]
    for i in range(0, len(file_events)):
        context = map_to_file_context(file_events[i])
        assert context == MOCK_FILE_CONTEXT[i]


def test_alert_get_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = alert_get_command(client, {"id": "36fb8ca5-0533-4d25-9763-e09d35d60610"})
    assert res["ruleId"] == "4576576e-13cb-4f88-be3a-ee77739de649"


def test_alert_resolve_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = alert_resolve_command(client, {"id": "36fb8ca5-0533-4d25-9763-e09d35d60610"})
    assert res["id"] == "36fb8ca5-0533-4d25-9763-e09d35d60610"


def test_departingemployee_add_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = departingemployee_add_command(
        client,
        {"username": "user1@example.com", "departuredate": "2020-01-01", "note": "Dummy note"},
    )
    expected_user_id = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected_user_id
    add_func = code42_sdk_mock.detectionlists.departing_employee.add
    add_func.assert_called_once_with(expected_user_id, departure_date="2020-01-01")
    code42_sdk_mock.detectionlists.update_user_notes.assert_called_once_with(
        expected_user_id, "Dummy note"
    )


def test_departingemployee_remove_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = departingemployee_remove_command(client, {"username": "user1@example.com"})
    expected = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected
    code42_sdk_mock.detectionlists.departing_employee.remove.assert_called_once_with(expected)


def test_departingemployee_get_all_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = departingemployee_get_all_command(client, {"username": "user1@example.com"})
    expected = json.loads(MOCK_GET_ALL_DEPARTING_EMPLOYEES_RESPONSE)["items"]
    assert res == expected
    assert code42_sdk_mock.detectionlists.departing_employee.get_all.call_count == 1


def test_departingemployee_get_all_command_gets_employees_from_multiple_pages(
    code42_sdk_mock, mocker
):
    # Setup get all departing employees
    page = MOCK_GET_ALL_DEPARTING_EMPLOYEES_RESPONSE
    # Setup 3 pages of employees
    employee_page_generator = (
        create_mock_code42_sdk_response(mocker, page) for page in [page, page, page]
    )
    code42_sdk_mock.detectionlists.departing_employee.get_all.return_value = employee_page_generator
    client = create_client(code42_sdk_mock)

    _, _, res = departingemployee_get_all_command(client, {"username": "user1@example.com"})

    # Expect to have employees from 3 pages in the result
    expected_page = json.loads(MOCK_GET_ALL_DEPARTING_EMPLOYEES_RESPONSE)["items"]
    expected = expected_page + expected_page + expected_page
    assert res == expected


def test_highriskemployee_add_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_add_command(
        client, {"username": "user1@example.com", "note": "Dummy note"}
    )
    expected_user_id = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected_user_id
    code42_sdk_mock.detectionlists.high_risk_employee.add.assert_called_once_with(expected_user_id)
    code42_sdk_mock.detectionlists.update_user_notes.assert_called_once_with(
        expected_user_id, "Dummy note"
    )


def test_highriskemployee_remove_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_remove_command(client, {"username": "user1@example.com"})
    expected = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected
    code42_sdk_mock.detectionlists.high_risk_employee.remove.assert_called_once_with(expected)


def test_highriskemployee_get_all_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_get_all_command(client, {})
    expected = json.loads(MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE)["items"]
    assert res == expected
    assert code42_sdk_mock.detectionlists.high_risk_employee.get_all.call_count == 1


def test_highriskemployee_get_all_command_gets_employees_from_multiple_pages(
    code42_sdk_mock, mocker
):
    # Setup get all high risk employees
    page = MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE
    # Setup 3 pages of employees
    employee_page_generator = (
        create_mock_code42_sdk_response(mocker, page) for page in [page, page, page]
    )
    code42_sdk_mock.detectionlists.high_risk_employee.get_all.return_value = employee_page_generator
    client = create_client(code42_sdk_mock)

    _, _, res = highriskemployee_get_all_command(client, {"username": "user1@example.com"})

    # Expect to have employees from 3 pages in the result
    expected_page = json.loads(MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE)["items"]
    expected = expected_page + expected_page + expected_page
    assert res == expected


def test_highriskemployee_get_all_command_when_given_risk_tags_only_gets_employees_with_tags(
    code42_sdk_mock
):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_get_all_command(
        client,
        {
            "risktags": [
                "PERFORMANCE_CONCERNS",
                "SUSPICIOUS_SYSTEM_ACTIVITY",
                "POOR_SECURITY_PRACTICES",
            ]
        },
    )
    # Only first employee has the given risk tags
    expected = [json.loads(MOCK_GET_ALL_HIGH_RISK_EMPLOYEES_RESPONSE)["items"][0]]
    assert res == expected
    assert code42_sdk_mock.detectionlists.high_risk_employee.get_all.call_count == 1


def test_highriskemployee_add_risk_tags_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_add_risk_tags_command(
        client, {"username": "user1@example.com", "risktags": "FLIGHT_RISK"}
    )
    expected_user_id = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected_user_id
    code42_sdk_mock.detectionlists.add_user_risk_tags.assert_called_once_with(
        expected_user_id, "FLIGHT_RISK"
    )


def test_highriskemployee_remove_risk_tags_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = highriskemployee_remove_risk_tags_command(
        client, {"username": "user1@example.com", "risktags": ["FLIGHT_RISK", "CONTRACT_EMPLOYEE"]}
    )
    expected_user_id = "123412341234123412"  # value found in GET_USER_RESPONSE
    assert res == expected_user_id
    code42_sdk_mock.detectionlists.remove_user_risk_tags.assert_called_once_with(
        expected_user_id, ["FLIGHT_RISK", "CONTRACT_EMPLOYEE"]
    )


def test_security_data_search_command(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    _, _, res = securitydata_search_command(client, MOCK_SECURITY_DATA_SEARCH_QUERY)
    assert len(res) == 3
    actual_query = code42_sdk_mock.securitydata.search_file_events.call_args[0][0]
    filter_groups = json.loads(str(actual_query))["groups"]
    assert filter_groups[0]["filters"][0]["term"] == "md5Checksum"
    assert filter_groups[0]["filters"][0]["value"] == "d41d8cd98f00b204e9800998ecf8427e"
    assert filter_groups[1]["filters"][0]["term"] == "osHostName"
    assert filter_groups[1]["filters"][0]["value"] == "DESKTOP-0001"
    assert filter_groups[2]["filters"][0]["term"] == "deviceUserName"
    assert filter_groups[2]["filters"][0]["value"] == "user3@example.com"
    assert filter_groups[3]["filters"][0]["term"] == "exposure"
    assert filter_groups[3]["filters"][0]["value"] == "ApplicationRead"


def test_fetch_incidents_handles_single_severity(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    fetch_incidents(
        client=client,
        last_run={"last_fetch": None},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter="High",
        fetch_limit=10,
        include_files=True,
        integration_context=None,
    )
    assert "HIGH" in str(code42_sdk_mock.alerts.search.call_args[0][0])


def test_fetch_incidents_handles_multi_severity(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    fetch_incidents(
        client=client,
        last_run={"last_fetch": None},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter=["High", "Low"],
        fetch_limit=10,
        include_files=True,
        integration_context=None,
    )
    assert "HIGH" in str(code42_sdk_mock.alerts.search.call_args[0][0])
    assert "LOW" in str(code42_sdk_mock.alerts.search.call_args[0][0])


def test_fetch_incidents_first_run(code42_sdk_mock):
    client = create_client(code42_sdk_mock)
    next_run, incidents, remaining_incidents = fetch_incidents(
        client=client,
        last_run={"last_fetch": None},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter=None,
        fetch_limit=10,
        include_files=True,
        integration_context=None,
    )
    assert len(incidents) == 3
    assert next_run["last_fetch"]


def test_fetch_incidents_next_run(code42_sdk_mock):
    mock_date = "2020-01-01T00:00:00.000Z"
    mock_timestamp = int(time.mktime(time.strptime(mock_date, "%Y-%m-%dT%H:%M:%S.000Z")))
    client = create_client(code42_sdk_mock)
    next_run, incidents, remaining_incidents = fetch_incidents(
        client=client,
        last_run={"last_fetch": mock_timestamp},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter=None,
        fetch_limit=10,
        include_files=True,
        integration_context=None,
    )
    assert len(incidents) == 3
    assert next_run["last_fetch"]


def test_fetch_incidents_fetch_limit(code42_sdk_mock):
    mock_date = "2020-01-01T00:00:00.000Z"
    mock_timestamp = int(time.mktime(time.strptime(mock_date, "%Y-%m-%dT%H:%M:%S.000Z")))
    client = create_client(code42_sdk_mock)
    next_run, incidents, remaining_incidents = fetch_incidents(
        client=client,
        last_run={"last_fetch": mock_timestamp},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter=None,
        fetch_limit=2,
        include_files=True,
        integration_context=None,
    )
    assert len(incidents) == 2
    assert next_run["last_fetch"]
    assert len(remaining_incidents) == 1
    # Run again to get the last incident
    next_run, incidents, remaining_incidents = fetch_incidents(
        client=client,
        last_run={"last_fetch": mock_timestamp},
        first_fetch_time=MOCK_FETCH_TIME,
        event_severity_filter=None,
        fetch_limit=2,
        include_files=True,
        integration_context={"remaining_incidents": remaining_incidents},
    )
    assert len(incidents) == 1
    assert next_run["last_fetch"]
    assert not remaining_incidents
