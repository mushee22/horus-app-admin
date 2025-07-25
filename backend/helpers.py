from web.models import Community


def add_to_community(student, batch, package):
    
    try:
        community_names = {
            'global': 'public_community',
            'batch': f'{batch.name}_community',
            'package': f'{package.title}_community'
        }

        for community_type, default_name in community_names.items():
            community, _ = Community.objects.get_or_create(
                default_name=default_name,
                defaults={
                    'name': default_name,
                    'type': community_type
                }
            )
            student.community.add(community)

        return True, None

    except Exception as e:
        return False, str(e)