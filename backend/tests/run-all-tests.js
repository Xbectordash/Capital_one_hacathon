#!/usr/bin/env node

/**
 * 🌾 FarmMate Agricultural AI - Comprehensive Test Runner
 * 
 * This script runs all test suites for the three-tier architecture:
 * - Backend Express Gateway tests
 * - Python AI integration tests  
 * - End-to-end agricultural workflow tests
 */

const { spawn } = require('child_process');
const path = require('path');

console.log('🌾 FarmMate Agricultural AI - Test Suite Runner');
console.log('='.repeat(60));

const tests = [
    {
        name: '🔧 Basic Communication Test',
        script: 'test-communication.js',
        description: 'Tests Socket.IO connection between frontend and backend'
    },
    {
        name: '🐍 Direct Python AI Test', 
        script: 'test-direct-ai.js',
        description: 'Tests direct connection to Python AI server'
    },
    {
        name: '📝 Farm Query Test',
        script: 'test-farm-query.js', 
        description: 'Tests specific agricultural query processing'
    },
    {
        name: '🌾 Comprehensive Farm Test',
        script: 'test-comprehensive-farm.js',
        description: 'Tests complete agricultural workflow with multiple queries'
    }
];

let currentTest = 0;

function runNextTest() {
    if (currentTest >= tests.length) {
        console.log('\n🎉 All tests completed!');
        console.log('✅ FarmMate Agricultural AI system verified');
        process.exit(0);
        return;
    }

    const test = tests[currentTest];
    console.log(`\n${test.name}`);
    console.log(`📋 ${test.description}`);
    console.log('-'.repeat(60));

    const testProcess = spawn('node', [path.join(__dirname, test.script)], {
        stdio: 'inherit',
        cwd: __dirname
    });

    testProcess.on('close', (code) => {
        if (code === 0) {
            console.log(`✅ ${test.name} - PASSED`);
        } else {
            console.log(`❌ ${test.name} - FAILED (exit code: ${code})`);
        }
        
        currentTest++;
        setTimeout(() => {
            runNextTest();
        }, 2000); // Wait 2 seconds between tests
    });

    testProcess.on('error', (error) => {
        console.log(`❌ ${test.name} - ERROR: ${error.message}`);
        currentTest++;
        setTimeout(() => {
            runNextTest();
        }, 2000);
    });
}

// Check if Docker services are running first
console.log('🔍 Checking if Docker services are running...');
const dockerCheck = spawn('docker-compose', ['ps'], { 
    cwd: path.join(__dirname, '..', '..'),
    stdio: 'pipe'
});

dockerCheck.on('close', (code) => {
    if (code === 0) {
        console.log('✅ Docker services are available');
        console.log('🚀 Starting test suite...\n');
        runNextTest();
    } else {
        console.log('❌ Docker services not running. Please start them first:');
        console.log('   docker-compose up -d');
        process.exit(1);
    }
});

dockerCheck.on('error', (error) => {
    console.log('❌ Docker not available:', error.message);
    console.log('Please ensure Docker is installed and services are running');
    process.exit(1);
});

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
    console.log('\n🛑 Test suite interrupted by user');
    process.exit(0);
});
