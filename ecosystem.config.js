module.exports = {
    apps: [{
        name: 'saya_bukan_bot',
        script: './server.py',
        autorestart: true,
        interpreter: './venv/bin/python',
    }],
};