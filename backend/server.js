const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true
}));
app.use(express.json());

const students = [
  {
    id: 1,
    name: 'Aarav Sharma',
    grade: 'Class 10-A',
    attendance: 96,
    average: 88,
    feeStatus: 'Paid',
    tracker: 'On track'
  },
  {
    id: 2,
    name: 'Meera Patel',
    grade: 'Class 9-B',
    attendance: 91,
    average: 84,
    feeStatus: 'Partial',
    tracker: 'Needs attention'
  },
  {
    id: 3,
    name: 'Vihaan Reddy',
    grade: 'Class 8-C',
    attendance: 94,
    average: 90,
    feeStatus: 'Paid',
    tracker: 'On track'
  }
];

const dashboard = {
  overview: {
    totalStudents: 15000,
    attendanceRate: 94.6,
    feeCollection: 87.4,
    activeTeachers: 540,
    averageMarks: 83.2
  },
  trends: [
    { month: 'Jan', attendance: 92, fees: 70 },
    { month: 'Feb', attendance: 93, fees: 74 },
    { month: 'Mar', attendance: 94, fees: 85 },
    { month: 'Apr', attendance: 95, fees: 81 },
    { month: 'May', attendance: 96, fees: 88 }
  ],
  alerts: [
    '12 students need attendance follow-up',
    'Fee reminders due for 48 families',
    '3 new grade submissions pending review'
  ]
};

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    app: 'School Student Information System',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/dashboard', (req, res) => {
  res.json(dashboard);
});

app.get('/api/students', (req, res) => {
  res.json(students);
});

app.get('/api/students/:id', (req, res) => {
  const student = students.find((item) => item.id === Number(req.params.id));

  if (!student) {
    return res.status(404).json({ message: 'Student not found' });
  }

  return res.json(student);
});

app.listen(port, () => {
  console.log(`School SIS API running on http://localhost:${port}`);
});
