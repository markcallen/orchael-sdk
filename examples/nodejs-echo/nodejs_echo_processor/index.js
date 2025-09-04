const express = require('express');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Simple echo processor class
class NodejsEchoProcessor {
    constructor() {
        this.history = [];
    }

    processChat(chatInput) {
        const input = chatInput.input;

        // Simple echo - just return the input
        const output = input;

        // Store in history
        this.history.push({
            input: input,
            output: output,
            timestamp: new Date().toISOString()
        });

        return {
            input: input,
            output: output
        };
    }

    getHistory() {
        return this.history;
    }
}

// Create processor instance
const processor = new NodejsEchoProcessor();

// Chat endpoint
app.post('/chat', (req, res) => {
    try {
        const chatInput = req.body;

        if (!chatInput.input) {
            return res.status(400).json({
                error: 'Missing input field'
            });
        }

        const result = processor.processChat(chatInput);
        res.json(result);
    } catch (error) {
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// History endpoint
app.get('/history', (req, res) => {
    try {
        const history = processor.getHistory();
        res.json(history);
    } catch (error) {
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(port, '0.0.0.0', () => {
    console.log(`Node.js Echo Agent running on port ${port}`);
    console.log(`Health check: http://localhost:${port}/health`);
    console.log(`Chat endpoint: http://localhost:${port}/chat`);
    console.log(`History endpoint: http://localhost:${port}/history`);
});

module.exports = { NodejsEchoProcessor };
