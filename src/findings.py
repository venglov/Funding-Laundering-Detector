from forta_agent import Finding, FindingType, FindingSeverity

from src.config import FUNDING_CRITICAL, FUNDING_HIGH, FUNDING_MEDIUM, LAUNDERING_CRITICAL, LAUNDERING_HIGH, \
    LAUNDERING_MEDIUM


def get_severity(usd):
    if usd > FUNDING_CRITICAL:
        return FindingSeverity.Critical
    elif usd > FUNDING_HIGH:
        return FindingSeverity.High
    elif usd > FUNDING_MEDIUM:
        return FindingSeverity.Medium
    else:
        return FindingSeverity.Low


def get_severity_laundering(usd):
    if usd > LAUNDERING_CRITICAL:
        return FindingSeverity.Critical
    elif usd > LAUNDERING_HIGH:
        return FindingSeverity.High
    elif usd > LAUNDERING_MEDIUM:
        return FindingSeverity.Medium
    else:
        return FindingSeverity.Low


class FundingLaunderingFindings:

    @staticmethod
    def funding(from_, to, usd, token, is_new, type_, tx_hash):
        return Finding({
            'name': f'Funding Alert',
            'description': f'{to} was funded using {type_ if not type_ == "unknown" else ""} {from_}',
            'alert_id': 'FLD_FUNDING',
            'type': FindingType.Suspicious,
            'severity': FindingSeverity.Critical if is_new else get_severity(usd),
            'metadata': {
                'funded_address': to,
                'newly_created': is_new,
                'source_address': from_,
                'source_type': type_,
                'usd_volume': usd,
                'token': token,
                'tx_hash': tx_hash,
            }
        })

    @staticmethod
    def laundering(from_, to, usd, token, is_new, type_, tx_hash):
        return Finding({
            'name': f'Laundering Alert',
            'description': f'{from_} is engaged in money laundering behavior using {type_ if not type_ == "unknown" else ""} {from_}',
            'alert_id': 'FLD_Laundering',
            'type': FindingType.Suspicious,
            'severity': get_severity_laundering(usd),
            'metadata': {
                'laundering_address': from_,
                'newly_created': is_new,
                'target_address': to,
                'target_type': type_,
                'usd_volume': usd,
                'token': token,
                'tx_hash': tx_hash,
            }
        })
