         // src/App.jsx
import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine } from 'recharts';
import './index.css';

const Dashboard = () => {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [dateRange, setDateRange] = useState({ start: '2010-01-01', end: '2025-08-01' });
  const [selectedEvent, setSelectedEvent] = useState(null);

  // Fetch data from Flask APIs
  useEffect(() => {
    fetch('/api/prices')
      .then(res => res.json())
      .then(data => setPrices(data))
      .catch(err => console.error('Error fetching prices:', err));
    fetch('/api/events')
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error('Error fetching events:', err));
    fetch('/api/change_points')
      .then(res => res.json())
      .then(data => setChangePoints(data))
      .catch(err => console.error('Error fetching change points:', err));
  }, []);

  // Filter data by date range
  const filteredPrices = prices.filter(p => {
    const date = new Date(p.Date);
    return date >= new Date(dateRange.start) && date <= new Date(dateRange.end);
  });

  // Calculate key indicators
  const volatility = prices.length > 0 
    ? (Math.max(...prices.map(p => p.Volatility || 0)).toFixed(2)) 
    : 0;
  const avgPriceChange = changePoints.length > 0 
    ? (changePoints.reduce((sum, cp) => sum + Math.abs(cp.Price_Change_Percent), 0) / changePoints.length).toFixed(2) 
    : 0;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Brent Oil Price Dashboard</h1>
      
      {/* Date Range Filter */}
      <div className="mb-4 flex flex-col sm:flex-row sm:space-x-4">
        <div className="mb-2 sm:mb-0">
          <label className="block text-sm font-medium">Start Date</label>
          <input
            type="date"
            value={dateRange.start}
            onChange={e => setDateRange({ ...dateRange, start: e.target.value })}
            className="border p-2 rounded w-full sm:w-auto"
          />
        </div>
        <div>
          <label className="block text-sm font-medium">End Date</label>
          <input
            type="date"
            value={dateRange.end}
            onChange={e => setDateRange({ ...dateRange, end: e.target.value })}
            className="border p-2 rounded w-full sm:w-auto"
          />
        </div>
      </div>

      {/* Key Indicators */}
      <div className="mb-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-gray-100 p-4 rounded">
          <h3 className="text-lg font-semibold">Max Volatility</h3>
          <p>{volatility}%</p>
        </div>
        <div className="bg-gray-100 p-4 rounded">
          <h3 className="text-lg font-semibold">Avg Price Change</h3>
          <p>{avgPriceChange}%</p>
        </div>
      </div>

      {/* Price Chart with Event Markers */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Brent Oil Price Trends</h2>
        <LineChart width={Math.min(window.innerWidth - 40, 800)} height={400} data={filteredPrices} className="mx-auto">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Date" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Brent_Price" stroke="#8884d8" name="Brent Price ($/bbl)" />
          {events.map(event => (
            <ReferenceLine
              key={event.Event_Name}
              x={event.Start_Date}
              stroke="red"
              label={{ value: event.Event_Name, position: 'top', fill: 'red', fontSize: 12 }}
              strokeDasharray="3 3"
            />
          ))}
          {changePoints.map(cp => (
            <ReferenceLine
              key={cp.Change_Point_Date}
              x={cp.Change_Point_Date}
              stroke="green"
              label={{ value: `Change Point (${cp.Associated_Events})`, position: 'top', fill: 'green', fontSize: 12 }}
            />
          ))}
        </LineChart>
      </div>

      {/* Event Table */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Events Impacting Brent Oil Prices</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse border">
            <thead>
              <tr className="bg-gray-200">
                <th className="border p-2 text-left">Event Name</th>
                <th className="border p-2 text-left">Type</th>
                <th className="border p-2 text-left">Date</th>
                <th className="border p-2 text-left">Description</th>
              </tr>
            </thead>
            <tbody>
              {events
                .filter(e => {
                  const date = new Date(e.Start_Date);
                  return date >= new Date(dateRange.start) && date <= new Date(dateRange.end);
                })
                .map(event => (
                  <tr
                    key={event.Event_Name}
                    className={selectedEvent === event.Event_Name ? 'bg-blue-100' : 'hover:bg-gray-50'}
                    onClick={() => setSelectedEvent(event.Event_Name)}
                  >
                    <td className="border p-2">{event.Event_Name}</td>
                    <td className="border p-2">{event.Event_Type}</td>
                    <td className="border p-2">{event.Start_Date}</td>
                    <td className="border p-2">{event.Description}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;