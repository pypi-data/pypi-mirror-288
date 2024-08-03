MAX_WORKERS = 10  # The number of parallel threads to be executed within the AWS Ops Toolkit package.

# The list of AWS regions
AWS_REGIONS = [
    {"code": "us-east-1", "name": "US East (N. Virginia)"},
    {"code": "us-east-2", "name": "US East (Ohio)"},
    {"code": "us-west-1", "name": "US West (N. California)"},
    {"code": "us-west-2", "name": "US West (Oregon)"},
    {"code": "af-south-1", "name": "Africa (Cape Town)"},
    {"code": "ap-east-1", "name": "Asia Pacific (Hong Kong)"},
    {"code": "ap-south-2", "name": "Asia Pacific (Hyderabad)"},
    {"code": "ap-southeast-3", "name": "Asia Pacific (Jakarta)"},
    {"code": "ap-southeast-4", "name": "Asia Pacific (Melbourne)"},
    {"code": "ap-south-1", "name": "Asia Pacific (Mumbai)"},
    {"code": "ap-northeast-3", "name": "Asia Pacific (Osaka)"},
    {"code": "ap-northeast-2", "name": "Asia Pacific (Seoul)"},
    {"code": "ap-southeast-1", "name": "Asia Pacific (Singapore)"},
    {"code": "ap-southeast-2", "name": "Asia Pacific (Sydney)"},
    {"code": "ap-northeast-1", "name": "Asia Pacific (Tokyo)"},
    {"code": "ca-central-1", "name": "Canada (Central)"},
    {"code": "ca-west-1", "name": "Canada West (Calgary)"},
    {"code": "eu-central-1", "name": "Europe (Frankfurt)"},
    {"code": "eu-west-1", "name": "Europe (Ireland)"},
    {"code": "eu-west-2", "name": "Europe (London)"},
    {"code": "eu-south-1", "name": "Europe (Milan)"},
    {"code": "eu-west-3", "name": "Europe (Paris)"},
    {"code": "eu-south-2", "name": "Europe (Spain)"},
    {"code": "eu-north-1", "name": "Europe (Stockholm)"},
    {"code": "eu-central-2", "name": "Europe (Zurich)"},
    {"code": "il-central-1", "name": "Israel (Tel Aviv)"},
    {"code": "me-south-1", "name": "Middle East (Bahrain)"},
    {"code": "me-central-1", "name": "Middle East (UAE)"},
    {"code": "sa-east-1", "name": "South America (Sao Paulo)"}
]

# The list of AWS region codes
AWS_REGION_CODES = [
    region.get('code') for region in AWS_REGIONS
]
