import demistomock as demisto
from CommonServerPython import *
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from libnmap.reportjson import ReportEncoder

if demisto.command() == "test-module":
    demisto.results("ok")
    sys.exit(0)
if demisto.command() == "nmap-scan":
    nm = NmapProcess(argToList(demisto.args()["targets"]), options=demisto.args()["options"])
    rc = nm.run()
    if rc != 0:
        demisto.results(
            {"Type": entryTypes["error"], "ContentsFormat": formats["text"], "Contents": "Unable to execute - " + nm.stderr}
        )
        sys.exit(0)
    r = NmapParser.parse(nm.stdout)
    md = "## " + r.summary + "\n"
    hosts = []

    try:
        scan_type = r.scan_type

    except KeyError:
        scan_type = None

    for host in r.hosts:
        h = {}
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
            h["Hostname"] = tmp_host
        else:
            tmp_host = host.address

        h["Address"] = host.address
        h["Status"] = host.status
        svc = []
        md += f"### Nmap scan report for {tmp_host}" + (f" ({host.address})\n" if tmp_host != host.address else "\n")
        md += f"#### Host is {host.status}.\n"
        for serv in host.services:
            svc.append(
                {
                    "Port": serv.port,
                    "Protocol": serv.protocol,
                    "State": serv.state,
                    "Service": serv.service,
                    "Banner": serv.banner,
                }
            )
        extras = []
        for hostscript in host._extras.get("hostscript", []):
            extras.append(
                {
                    "ID": hostscript.get("id"),
                    "Output": hostscript.get("output"),
                    "Elements": hostscript.get("elements"),
                }
            )
        md += tableToMarkdown("Services", svc, ["Port", "Protocol", "State", "Service", "Banner"])
        md += tableToMarkdown("Script Results", extras, ["ID", "Output", "Elements"])
        h["Services"] = svc
        h["ScriptResults"] = extras
        hosts.append(h)
    scan = {
        "Summary": r.summary,
        "Version": r.version,
        "Started": r.started,
        "Ended": r.endtime,
        "CommandLine": r.commandline,
        "ScanType": scan_type,
        "Hosts": hosts,
    }
    demisto.results(
        {
            "ContentsFormat": formats["json"],
            "Type": entryTypes["note"],
            "Contents": json.dumps(r, cls=ReportEncoder),
            "HumanReadable": md,
            "EntryContext": {"NMAP.Scan": scan},
        }
    )
