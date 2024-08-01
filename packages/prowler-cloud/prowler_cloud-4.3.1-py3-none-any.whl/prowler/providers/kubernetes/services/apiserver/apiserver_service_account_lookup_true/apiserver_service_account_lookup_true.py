from prowler.lib.check.models import Check, Check_Report_Kubernetes
from prowler.providers.kubernetes.services.apiserver.apiserver_client import (
    apiserver_client,
)


class apiserver_service_account_lookup_true(Check):
    def execute(self) -> Check_Report_Kubernetes:
        findings = []
        for pod in apiserver_client.apiserver_pods:
            report = Check_Report_Kubernetes(self.metadata())
            report.namespace = pod.namespace
            report.resource_name = pod.name
            report.resource_id = pod.uid
            report.status = "PASS"
            report.status_extended = (
                f"Service account lookup is set to true in pod {pod.name}."
            )

            for container in pod.containers.values():
                # Check if "--service-account-lookup" is set to true
                if "--service-account-lookup=true" not in str(container.command):
                    report.status = "FAIL"
                    report.status_extended = (
                        f"Service account lookup is not set to true in pod {pod.name}."
                    )
                    break

            findings.append(report)
        return findings
