module.exports = {
    apps: [{
        name: 'multi-channel-bot',
        script: './server.py',
        interpreter: './venv/bin/python',
        autorestart: true,
    }, ],
};