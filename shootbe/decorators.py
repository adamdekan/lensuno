def is_freelancer(user):
    return user.groups.filter(name="freelancer").exists()
