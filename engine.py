"""Evaluate typed automation capabilities with default-deny access."""
import json

def analyze(data):
    now = data['now']
    request = data['request']
    matches = [g for g in data.get('grants', [])
               if g['subject'] == request['subject'] and g['action'] == request['action']
               and g['resource'] == request['resource'] and g['expires'] > now]
    if any(g.get('effect') == 'deny' for g in matches):
        return {'allowed': False, 'reason': 'explicit-deny'}
    allowed = [g for g in matches if g.get('effect') == 'allow']
    if not allowed:
        return {'allowed': False, 'reason': 'no-active-grant'}
    if all(g.get('approval_required', False) for g in allowed) and not request.get('approved', False):
        return {'allowed': False, 'reason': 'approval-required'}
    return {'allowed': True, 'reason': 'active-grant'}

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Path to a JSON scenario')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError('Input must be a JSON object')
        print(json.dumps(analyze(data), indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, OSError) as error:
        print('Input error: '+str(error), file=sys.stderr)
        sys.exit(2)
