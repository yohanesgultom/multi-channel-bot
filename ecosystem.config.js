module.exports = {
    apps: [{
            name: 'multi-channel-bot',
            script: './server.py',
            interpreter: './venv/bin/python',
            autorestart: true,
        },
        {
            name: 'multi-channel-bot-jobs',
            script: './settings.py', // does nothing
            interpreter: './venv/bin/python',
            interpreter_args: '-m channel.telegram.jobs',
            cron_restart: '*/30 * * * *',
            autorestart: false,
        }
    ],
};