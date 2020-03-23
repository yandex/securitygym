import epicbox


def check(profile, command, files):
    epicbox.configure(
        profiles=[
            epicbox.Profile('python', 'security-gym-python'),
            epicbox.Profile('javascript', 'security-gym-javascript')
        ]
    )
    limits = {'cputime': 10, 'memory': 128}
    result = epicbox.run(profile,
                         command,
                         files=files, limits=limits)
    return result
