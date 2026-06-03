import requests


class ClinicalTrialsAPI:
    """
    Simple ClinicalTrials.gov API client.

    This module searches public clinical trial records by condition
    and returns clean trial information for the Streamlit app.
    """

    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

    def search_trials(self, condition: str, max_results: int = 10):
        if not condition or not condition.strip():
            return []

        params = {
            "query.cond": condition.strip(),
            "pageSize": max_results,
            "format": "json",
        }

        response = requests.get(self.BASE_URL, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()
        studies = data.get("studies", [])

        results = []

        for study in studies:
            protocol = study.get("protocolSection", {})

            identification = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            conditions = protocol.get("conditionsModule", {})
            design = protocol.get("designModule", {})
            arms = protocol.get("armsInterventionsModule", {})
            contacts = protocol.get("contactsLocationsModule", {})

            nct_id = identification.get("nctId", "N/A")
            title = identification.get("briefTitle", "No title available")
            overall_status = status.get("overallStatus", "Unknown")

            condition_list = conditions.get("conditions", [])
            intervention_list = arms.get("interventions", [])

            interventions = []
            for intervention in intervention_list:
                name = intervention.get("name")
                if name:
                    interventions.append(name)

            locations = contacts.get("locations", [])
            location_text = "Not listed"

            if locations:
                first_location = locations[0]
                city = first_location.get("city", "")
                state = first_location.get("state", "")
                country = first_location.get("country", "")

                location_parts = [part for part in [city, state, country] if part]
                if location_parts:
                    location_text = ", ".join(location_parts)

            phases = design.get("phases", [])
            phase_text = ", ".join(phases) if phases else "Not listed"

            trial_url = f"https://clinicaltrials.gov/study/{nct_id}"

            results.append(
                {
                    "nct_id": nct_id,
                    "title": title,
                    "status": overall_status,
                    "conditions": condition_list,
                    "interventions": interventions,
                    "phase": phase_text,
                    "location": location_text,
                    "url": trial_url,
                    "match_reason": (
                        f"This trial may be relevant because it is listed under "
                        f"conditions related to '{condition.strip()}'."
                    ),
                }
            )

        return results


if __name__ == "__main__":
    api = ClinicalTrialsAPI()
    trials = api.search_trials("diabetes", max_results=3)

    for trial in trials:
        print("=" * 80)
        print(trial["nct_id"])
        print(trial["title"])
        print(trial["status"])
        print(trial["url"])