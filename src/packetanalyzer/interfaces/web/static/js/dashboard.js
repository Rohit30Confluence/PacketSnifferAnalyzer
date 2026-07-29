/**
 * PacketSnifferAnalyzer Dashboard — Client-side JavaScript
 *
 * Handles:
 *   - Alpine.js data component (dashboard())
 *   - WebSocket connection for real-time packet stream
 *   - Chart.js chart initialization and updates
 *   - Keyboard navigation
 *
 * Full implementation in Phase 3 (M5).
 */

'use strict';

/**
 * Alpine.js dashboard data component.
 * @returns {Object} The Alpine.js component data and methods.
 */
function dashboard() {
    return {
        // State
        capturing: false,
        selectedInterface: '',
        bpfFilter: '',
        status: 'Idle',
        stats: {
            totalPackets: 0,
            pps: 0,
            bps: 0,
            dropped: 0,
        },

        // WebSocket
        ws: null,

        init() {
            this.initCharts();
            this.connectWebSocket();
            this.loadInterfaces();
        },

        initCharts() {
            // PPS chart
            const ppsCtx = document.getElementById('ppsChart');
            if (ppsCtx) {
                this.ppsChart = new Chart(ppsCtx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [{
                            label: 'Packets/s',
                            data: [],
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            tension: 0.4,
                            fill: true,
                        }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        animation: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { display: false },
                            y: { beginAtZero: true, grid: { color: '#1f2937' } },
                        },
                    },
                });
            }

            // Protocol distribution chart
            const protoCtx = document.getElementById('protocolChart');
            if (protoCtx) {
                this.protoChart = new Chart(protoCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['TCP', 'UDP', 'ICMP', 'DNS', 'Other'],
                        datasets: [{
                            data: [0, 0, 0, 0, 0],
                            backgroundColor: [
                                '#60a5fa', '#34d399', '#f87171', '#a78bfa', '#9ca3af',
                            ],
                        }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: { color: '#9ca3af', font: { size: 11 } },
                            },
                        },
                    },
                });
            }
        },

        connectWebSocket() {
            // Full WebSocket implementation in Phase 3 (M5)
            console.info('WebSocket connection will be established in Phase 3 (M5).');
        },

        loadInterfaces() {
            // Full interface loading in Phase 3 (M5)
            console.info('Interface loading will be implemented in Phase 3 (M5).');
        },
    };
}
