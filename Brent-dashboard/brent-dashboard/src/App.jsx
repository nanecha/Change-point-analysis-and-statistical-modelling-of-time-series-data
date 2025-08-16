import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import dayjs from 'dayjs'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ReferenceDot, ReferenceArea
} from 'recharts'

export default function App() {
  // ✅ Default dates for immediate loading
  const [start, setStart] = useState('2025-08-01')
  const [end, setEnd] = useState('2025-08-10')
  const [roll, setRoll] = useState(0)
  const [eventWindow, setEventWindow] = useState(3)
  const [eventType, setEventType] = useState('')
  
  const [prices, setPrices] = useState([])
  const [forecast, setForecast] = useState([])
  const [events, setEvents] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [highlight, setHighlight] = useState(null)

  // --- Dummy fallback data ---
  const dummyPrices = [
    { date: '2025-08-01', price: 78.2 },
    { date: '2025-08-02', price: 78.9 },
    { date: '2025-08-03', price: 79.4 },
    { date: '2025-08-04', price: 79.0 },
    { date: '2025-08-05', price: 80.1 },
    { date: '2025-08-06', price: 80.6 },
    { date: '2025-08-07', price: 80.2 },
  ]
  const dummyForecast = [
    { date: '2025-08-08', forecast: 80.7 },
    { date: '2025-08-09', forecast: 80.9 },
    { date: '2025-08-10', forecast: 81.2 },
  ]
  const dummyEvents = [
    { date: '2025-08-03', event_type: 'geopolitical', title: 'Regional tension rises' },
    { date: '2025-08-05', event_type: 'policy_sanction', title: 'OPEC+ surprise comment' },
  ]
  const dummyMetrics = {
    annualized_volatility: 0.05,
    counts: { prices: dummyPrices.length, events: dummyEvents.length },
    event_impacts: [
      { date: '2025-08-03', title: 'Regional tension rises', event_type: 'geopolitical', avg_window_price: 79.25, event_delta: 0.015 },
      { date: '2025-08-05', title: 'OPEC+ surprise comment', event_type: 'policy_sanction', avg_window_price: 79.9, event_delta: 0.012 },
    ]
  }

  // --- Fetch data from API or fallback to dummy ---
  const fetchAll = async () => {
    try {
      const params = { start, end }
      const qp = new URLSearchParams(params)
      const [p, f, e] = await Promise.all([
        axios.get(`/api/prices?${qp}${roll ? `&roll=${roll}` : ''}`),
        axios.get(`/api/forecast?${qp}`),
        axios.get(`/api/events?${qp}${eventType ? `&type=${eventType}` : ''}`)
      ])
      setPrices(p.data)
      setForecast(f.data)
      setEvents(e.data)

      const m = await axios.get(`/api/metrics?event_window=${eventWindow}`)
      setMetrics(m.data)
    } catch (err) {
      console.warn('API unavailable, using dummy data')
      setPrices(dummyPrices)
      setForecast(dummyForecast)
      setEvents(dummyEvents)
      setMetrics(dummyMetrics)
    }
  }

  useEffect(() => { fetchAll() }, [])

  // --- Merge price + forecast for chart ---
  const dataMerged = useMemo(() => {
    const map = new Map()
    prices.forEach(d => map.set(d.date, { date: d.date, price: d.price, price_smooth: d.price_smooth }))
    forecast.forEach(d => {
      const obj = map.get(d.date) || { date: d.date }
      obj.forecast = d.forecast
      map.set(d.date, obj)
    })
    return Array.from(map.values()).sort((a,b) => a.date.localeCompare(b.date))
  }, [prices, forecast])

  const eventTypes = Array.from(new Set(events.map(e => e.event_type))).filter(Boolean)

  const onSelectHighlight = (dateStr) => {
    if (!dateStr) return setHighlight(null)
    const d = dayjs(dateStr)
    const startH = d.subtract(eventWindow, 'day').format('YYYY-MM-DD')
    const endH = d.add(eventWindow, 'day').format('YYYY-MM-DD')
    setHighlight({ start: startH, end: endH })
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
        <div className="max-w-7xl mx-auto p-4 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-2xl font-bold">Brent Oil Dashboard</h1>
            <p className="text-sm text-slate-600">Explore trends, forecasts, and event impacts</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
            <div className="col-span-1">
              <label className="block text-xs">Start</label>
              <input type="date" value={start} onChange={e=>setStart(e.target.value)} className="w-full border rounded-xl p-2" />
            </div>
            <div className="col-span-1">
              <label className="block text-xs">End</label>
              <input type="date" value={end} onChange={e=>setEnd(e.target.value)} className="w-full border rounded-xl p-2" />
            </div>
            <div className="col-span-1">
              <label className="block text-xs">Roll (days)</label>
              <input type="number" value={roll} min={0} onChange={e=>setRoll(Number(e.target.value))} className="w-full border rounded-xl p-2" />
            </div>
            <div className="col-span-1">
              <label className="block text-xs">Event window (±days)</label>
              <input type="number" value={eventWindow} min={0} onChange={e=>setEventWindow(Number(e.target.value))} className="w-full border rounded-xl p-2" />
            </div>
            <div className="col-span-1">
              <label className="block text-xs">Event type</label>
              <select value={eventType} onChange={e=>setEventType(e.target.value)} className="w-full border rounded-xl p-2">
                <option value="">All</option>
                {eventTypes.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div className="col-span-1 flex items-end">
              <button onClick={fetchAll} className="w-full rounded-2xl px-4 py-2 bg-slate-900 text-white hover:bg-slate-800">Apply</button>
            </div>
          </div>
        </div>
      </header>

      {/* Chart and KPIs remain the same as your previous code */}
      {/* ...rest of your JSX */}
    </div>
  )
}
