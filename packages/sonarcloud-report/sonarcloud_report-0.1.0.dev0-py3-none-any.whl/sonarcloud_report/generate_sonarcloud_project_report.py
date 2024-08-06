from sonarqube import SonarCloudClient
from dataclasses import dataclass
from jinja2 import Template
import logging
import os

@dataclass
class SonarCloudProjectReport:
    project_name: str
    last_analysis_date: str
    last_analysis_commit_id: str
    bugs: int
    code_smells: int
    coverage: float
    security_hotspots: int
    vulnerabilities: int

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.last_analysis_date = ""
        self.last_analysis_commit_id = ""
        self.bugs = 0
        self.code_smells = 0
        self.coverage = 0
        self.security_hotspots = 0
        self.vulnerabilities = 0


_template = """# SonarCloud report for **{{ project_name }}**

- Project name: `{{ project_name }}`
- Analysis date: {{ last_analysis_date }}
- Analyzed commit ID: `{{ last_analysis_commit_id }}`

## SonarCloud metrics

| Metric name       | Description                                                                                          | Value                   |
| ----------------- | ---------------------------------------------------------------------------------------------------- | ----------------------- |
| Bugs              | A coding error that can break the code and needs to be fixed.                                        | {{ bugs }}              |
| Code coverage     | The percentage of lines of code covered by tests.                                                    | {{ coverage }}%         |
| Code smells       | Code that is confusing and can be difficult to maintain.                                             | {{ code_smells }}       |
| Security hotspots | Security-sensitive code that requires manual review to assess whether or not a vulnerability exists. | {{ security_hotspots }} |
| Vulnerabilities   | Code that can be exploited by hackers.                                                               | {{ vulnerabilities }}   |
"""

def query_sonarcloud_project_report(project_name: str, token: str) -> SonarCloudProjectReport:
    logging.info(f"Querying SonarCloud project info for '{project_name}'")
    client = SonarCloudClient(sonarqube_url="https://sonarcloud.io", token=token)

    project_infos = client.projects.get_project(key=f"lupindental_{project_name}", organization="lupindental")

    logging.info(f"Querying latest analysis details for '{project_name}'")
    project_measures = client.measures.get_component_with_specified_measures(
        component=f"lupindental_{project_name}",
        branch="main",
        metricKeys="bugs,code_smells,coverage,security_hotspots,vulnerabilities")
    assert project_measures["component"]["name"] == project_name

    result = SonarCloudProjectReport(project_name)
    result.last_analysis_date = project_infos["lastAnalysisDate"]
    result.last_analysis_commit_id = project_infos["revision"]

    # fill measures
    filled_measures = 0
    for m in project_measures["component"]["measures"]:
        match m["metric"]:
            case "bugs":
                result.bugs = int(m["value"])
                filled_measures += 1
            case "code_smells":
                result.code_smells = int(m["value"])
                filled_measures += 1
            case "coverage":
                result.coverage = float(m["value"])
                assert result.coverage <= 100
                filled_measures += 1
            case "security_hotspots":
                result.security_hotspots = int(m["value"])
                filled_measures += 1
            case "vulnerabilities":
                result.vulnerabilities = int(m["value"])
                filled_measures += 1
    assert filled_measures == 5

    return result

def generate_sonarcloud_project_report_file(project_name: str, sonar_token: str):
    if not project_name:
        logging.critical("Project name is missing, please define CI_PROJECT_NAME")
        exit(1)
    else:
        logging.info(f"Project name is '{project_name}'")

    if not sonar_token:
        logging.critical("SonarCloud token is missing")
        exit(1)

    #if not commit_id:
    #    logging.critical("Current commit ID is missing, please define CI_COMMIT_SHA")
    #    exit(1)
    #else:
    #    logging.info(f"Git commit ID is '{commit_id}'")
    #
    #branch_name = os.environ.get("CI_COMMIT_BRANCH")
    #tag_name = os.environ.get("CI_COMMIT_TAG")
    #if not branch_name:
    #    if tag_name:
    #        logging.info(f"Current build is for tag '{tag_name}'")
    #    else:
    #        logging.critical("Current build branch or tag name is missing, please define CI_COMMIT_BRANCH or CI_COMMIT_TAG")
    #        exit(1)
    #elif branch_name != "main":
    #    logging.critical(f"Current build branch must be 'main' or a tag, found '{branch_name}'")
    #    exit(1)
    #else:
    #    logging.info(f"Current build branch is '{branch_name}'")

    # TODO: pass tag name, and commit id?
    project_report = query_sonarcloud_project_report(project_name=project_name, token=sonar_token)

    logging.info("Generating output from report template")
    j2_template = Template(_template)
    rendered_text = j2_template.render(vars(project_report))

    output_file_name = "sonarcloud-report.md"
    logging.info(f"Saving output to file '{output_file_name}'")
    with open(output_file_name, "w") as f:
        f.write(rendered_text)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
generate_sonarcloud_project_report_file(
    project_name="lupin_core", # os.environ.get("CI_PROJECT_NAME")
    #commit_id=os.environ.get("CI_COMMIT_SHA"),
    sonar_token="ba9a92c9daf032e6831f6f739c242cdb1b0b0b2c" #os.environ.get("SONAR_TOKEN")
)
