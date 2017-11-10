from configuration.models import PrincipalInvestigator


def principal_investigator_name():
    principal_investigator = PrincipalInvestigator.get_solo()
    principal_investigator = principal_investigator.name
    return principal_investigator
