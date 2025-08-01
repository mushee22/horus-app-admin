# from web.models import Community


def add_to_community(student, Batch, Package):
    
    try:
        community_names = {
            'global': 'public_community',
            'batch': f'{Batch.name}_community',
            'package': f'{Package.title}_community'
        }

        for community_type, default_name in community_names.items():
            community, _ = Community.objects.get_or_create(
                default_name=default_name,
                defaults={
                    'name': default_name,
                    'type': community_type,
                    'batch':Batch,  # Batch is an instance
                    'package':Package # Package is an instance
                }
            )
            student.community.add(community)

        return True, None

    except Exception as e:
        return False, str(e)