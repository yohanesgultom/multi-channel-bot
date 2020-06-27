import unittest
from fabric import task

@task
def deploy(c):
    if test():
        print('Deploying...')
        with c.cd('~/multi-channel-bot'):
            c.run('git pull origin master')
            c.run('pm2 restart ecosystem.config.js')

def test():
    print('Testing...')
    loader = unittest.TestLoader()
    tests = loader.discover('test')
    testRunner = unittest.runner.TextTestRunner()
    result = testRunner.run(tests)
    return len(result.failures) == 0