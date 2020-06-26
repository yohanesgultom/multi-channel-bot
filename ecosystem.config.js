module.exports = {
    apps: [{
            name: 'saya_bukan_bot',
            script: './server.py',
            interpreter: './venv/bin/python',
            autorestart: true,
        },
        {
            name: 'saya_bukan_bot_jobs',
            script: '-m channel.telegram.jobs',
            interpreter: './venv/bin/python',
            cron_restart: '*/30 * * * *'
        }
    ],
};