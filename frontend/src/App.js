import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { BrowserRouter, Routes, Route } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Mobile detection hook
const useIsMobile = () => {
  const [isMobile, setIsMobile] = useState(false);
  
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  return isMobile;
};

// Dashboard Component
const Dashboard = () => {
  const [stats, setStats] = useState({
    total_reports: 0,
    active_cases: 0,
    alerts: 0,
    water_quality_average: 0,
    doctors_available: 0,
    critical_stocks: 0
  });
  const [recentReports, setRecentReports] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [waterQualityData, setWaterQualityData] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [medicalStock, setMedicalStock] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const isMobile = useIsMobile();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, reportsRes, waterRes, doctorsRes, stockRes] = await Promise.all([
        axios.get(`${API}/dashboard/stats`),
        axios.get(`${API}/reports?limit=15`),
        axios.get(`${API}/water-quality?limit=15`),
        axios.get(`${API}/doctors`),
        axios.get(`${API}/medical-stock`)
      ]);
      
      setStats(statsRes.data);
      setRecentReports(reportsRes.data);
      setWaterQualityData(waterRes.data);
      setDoctors(doctorsRes.data);
      setMedicalStock(stockRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Show user-friendly error message
      alert('Unable to load data. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReportSubmit = async (reportData) => {
    try {
      await axios.post(`${API}/reports`, reportData);
      setShowReportModal(false);
      fetchDashboardData();
    } catch (error) {
      console.error('Error submitting report:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getWaterStatusColor = (status) => {
    switch (status) {
      case 'safe': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'unsafe': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      {/* Navigation Bar */}
      <nav className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b px-4 md:px-6 py-3 md:py-4 relative`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3 md:space-x-4">
            {/* Mobile menu button */}
            {isMobile && (
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-colors`}
              >
                {sidebarOpen ? '✕' : '☰'}
              </button>
            )}
            <img 
              src="https://images.unsplash.com/photo-1630431174988-d3221f327b17?w=40&h=40&fit=crop&crop=center" 
              alt="Health Monitor Logo" 
              className="w-8 h-8 md:w-10 md:h-10 rounded-lg object-cover"
            />
            <h1 className={`text-lg md:text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'} truncate`}>
              Rural Health Monitor
            </h1>
          </div>
          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Refresh button */}
            <button
              onClick={fetchDashboardData}
              disabled={loading}
              className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-colors disabled:opacity-50`}
            >
              {loading ? <span className="animate-spin">⟳</span> : '🔄'}
            </button>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 text-white hover:bg-gray-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-colors`}
            >
              {darkMode ? '☀️' : '🌙'}
            </button>
            {!isMobile && (
              <div className="flex items-center space-x-2">
                <div className={`w-8 h-8 rounded-full ${darkMode ? 'bg-blue-600' : 'bg-blue-500'} flex items-center justify-center text-white font-semibold text-sm`}>
                  A
                </div>
                <span className={`${darkMode ? 'text-white' : 'text-gray-900'} text-sm`}>Admin User</span>
              </div>
            )}
          </div>
        </div>
      </nav>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`w-64 h-screen ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-r p-6`}>
          <nav className="space-y-2">
            {[
              { id: 'dashboard', icon: '📊', label: 'Dashboard' },
              { id: 'reports', icon: '📋', label: 'Health Reports' },
              { id: 'water-quality', icon: '💧', label: 'Water Quality' },
              { id: 'doctors', icon: '👨‍⚕️', label: 'Doctor Directory' },
              { id: 'stock', icon: '💊', label: 'Medical Stock' },
              { id: 'settings', icon: '⚙️', label: 'Settings' }
            ].map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  activeTab === item.id
                    ? (darkMode ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white')
                    : (darkMode ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-700 hover:bg-gray-100')
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border p-6 shadow-sm`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Total Reports</p>
                      <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{stats.total_reports}</p>
                    </div>
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-blue-600 text-xl">📋</span>
                    </div>
                  </div>
                </div>

                <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border p-6 shadow-sm`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Active Cases</p>
                      <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{stats.active_cases}</p>
                    </div>
                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                      <span className="text-orange-600 text-xl">🚨</span>
                    </div>
                  </div>
                </div>

                <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border p-6 shadow-sm`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Alerts</p>
                      <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{stats.alerts}</p>
                    </div>
                    <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                      <span className="text-red-600 text-xl">⚠️</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Reports Table */}
              <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border shadow-sm`}>
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Recent Health Reports</h2>
                    <button
                      onClick={() => setShowReportModal(true)}
                      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Submit New Report
                    </button>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className={`${darkMode ? 'border-gray-700' : 'border-gray-200'} border-b`}>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Reporter</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Symptoms</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Severity</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Date</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {recentReports.map((report, index) => (
                        <tr key={report.id || index} className={`${darkMode ? 'border-gray-700' : 'border-gray-200'} border-b last:border-b-0`}>
                          <td className={`px-6 py-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            {report.is_anonymous ? 'Anonymous' : report.reporter_name}
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {report.symptoms.length > 50 ? `${report.symptoms.substring(0, 50)}...` : report.symptoms}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(report.severity)}`}>
                              {report.severity}
                            </span>
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {formatDate(report.date_reported)}
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {report.status}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'water-quality' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Water Quality Monitoring</h2>
              </div>
              
              <div className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border shadow-sm`}>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className={`${darkMode ? 'border-gray-700' : 'border-gray-200'} border-b`}>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Location</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>TDS (ppm)</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>pH Level</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Status</th>
                        <th className={`text-left px-6 py-3 text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Test Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {waterQualityData.map((data, index) => (
                        <tr key={data.id || index} className={`${darkMode ? 'border-gray-700' : 'border-gray-200'} border-b last:border-b-0`}>
                          <td className={`px-6 py-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            {data.location?.address || 'Unknown Location'}
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {data.tds_value}
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {data.ph_level}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getWaterStatusColor(data.status)}`}>
                              {data.status}
                            </span>
                          </td>
                          <td className={`px-6 py-4 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                            {formatDate(data.test_date)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'doctors' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Doctor Directory</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {doctors.map((doctor, index) => (
                  <div key={doctor.id || index} className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl border p-6 shadow-sm`}>
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-blue-600 text-xl">👨‍⚕️</span>
                      </div>
                      <div className="flex-1">
                        <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{doctor.name}</h3>
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{doctor.specialization}</p>
                      </div>
                    </div>
                    <div className="mt-4 space-y-2">
                      <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                        <span className="font-medium">Phone:</span> {doctor.phone}
                      </p>
                      <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                        <span className="font-medium">Available:</span> {doctor.availability}
                      </p>
                      {doctor.clinic_name && (
                        <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                          <span className="font-medium">Clinic:</span> {doctor.clinic_name}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Report Modal */}
      {showReportModal && (
        <ReportModal 
          onClose={() => setShowReportModal(false)}
          onSubmit={handleReportSubmit}
          darkMode={darkMode}
        />
      )}
    </div>
  );
};

// Report Modal Component
const ReportModal = ({ onClose, onSubmit, darkMode }) => {
  const [formData, setFormData] = useState({
    reporter_name: '',
    report_type: 'disease',
    symptoms: '',
    severity: 'low',
    location: {
      lat: 0,
      lng: 0,
      address: ''
    },
    is_anonymous: false,
    additional_info: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Generate mock coordinates for demo
    const mockLocation = {
      lat: 28.7041 + (Math.random() - 0.5) * 0.1,
      lng: 77.1025 + (Math.random() - 0.5) * 0.1,
      address: formData.location.address || 'Rural Area, India'
    };
    
    onSubmit({
      ...formData,
      location: mockLocation
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto`}>
        <div className="flex items-center justify-between mb-4">
          <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Submit Health Report</h3>
          <button
            onClick={onClose}
            className={`text-gray-500 hover:text-gray-700 ${darkMode ? 'hover:text-gray-300' : ''}`}
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Reporter Name
            </label>
            <input
              type="text"
              value={formData.reporter_name}
              onChange={(e) => setFormData({...formData, reporter_name: e.target.value})}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'
              }`}
              required
            />
          </div>

          <div>
            <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Report Type
            </label>
            <select
              value={formData.report_type}
              onChange={(e) => setFormData({...formData, report_type: e.target.value})}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'
              }`}
            >
              <option value="disease">Disease Report</option>
              <option value="water_quality">Water Quality Issue</option>
              <option value="complaint">Anonymous Complaint</option>
            </select>
          </div>

          <div>
            <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Symptoms/Description
            </label>
            <textarea
              value={formData.symptoms}
              onChange={(e) => setFormData({...formData, symptoms: e.target.value})}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'
              }`}
              rows="3"
              required
            />
          </div>

          <div>
            <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Severity Level
            </label>
            <select
              value={formData.severity}
              onChange={(e) => setFormData({...formData, severity: e.target.value})}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'
              }`}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <div>
            <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Location/Address
            </label>
            <input
              type="text"
              value={formData.location.address}
              onChange={(e) => setFormData({
                ...formData, 
                location: {...formData.location, address: e.target.value}
              })}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-900'
              }`}
              placeholder="Enter your location"
            />
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="anonymous"
              checked={formData.is_anonymous}
              onChange={(e) => setFormData({...formData, is_anonymous: e.target.checked})}
              className="mr-2"
            />
            <label htmlFor="anonymous" className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
              Submit anonymously
            </label>
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className={`flex-1 px-4 py-2 border rounded-lg ${
                darkMode 
                  ? 'border-gray-600 text-gray-300 hover:bg-gray-700' 
                  : 'border-gray-300 text-gray-700 hover:bg-gray-50'
              } transition-colors`}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Submit Report
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;