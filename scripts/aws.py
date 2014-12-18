import boto.ec2

aws_creds = {
  'aws_access_key_id': 'AKIAJVOE6DLZEOINQRJQ',
  'aws_secret_access_key': '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'
}

conn = boto.ec2.connect_to_region("us-east-1", **aws_creds)
# see http://docs.pythonboto.org/en/latest/ec2_tut.html

def start_instances(count):
  e = conn.run_instances(
    'ami-c65b39ae',
    key_name='aws_promedia',
    instance_type='t2.micro',
    subnet_id='subnet-1c07ef37',
    security_group_ids=['sg-99c634fd'],
    min_count=count,
    max_count=count
  )
  return e

def stop_instance_by_ip(ip):
  res = conn.get_all_reservations()
  instances = []
  for r in res:
    instances.extend(r.instances)
  for i in instances:
    if i.ip_address == ip:
      stop_instances([i.id])

def stop_instances(list_of_ids):
  e = conn.terminate_instances(instance_ids=list_of_ids)
  return e