// Structured version of docs/CV_SOURCE.md for the Resume tab UI.
export interface ResumeJob {
  company: string
  title: string
  dates: string
  bullets: string[]
}

export const summary =
  "MBA with 14+ years in the service industry. Led call center teams of 130-165+ service experts plus 8+ vendors, working across IVR, email bots, speech analytics, and CRM development to turn service centers into profitable, compliant, customer-first operations."

export const jobs: ResumeJob[] = [
  {
    company: 'Quick Heal',
    title: 'Digital Revenue Lead',
    dates: 'Sept 2025 - Present',
    bullets: [
      'Own the customer lifecycle end to end — service, retention, cross-sell and up-sell',
      "Leading the shift from pure service to 'Service + AI'",
      'Driving automation-based revenue generation and frontline upskilling for the AI era',
    ],
  },
  {
    company: 'Parag Milk Foods Limited',
    title: 'Head Customer Service',
    dates: 'Dec 2024 - Sept 2025',
    bullets: [
      'Led call center operations across Phone, Chat & Email',
      'Salesforce 360 & chat bot development; MBR/QBR performance reporting',
      'Drove digital transformation — CRM, IVR, Ebots, speech analytics',
    ],
  },
  {
    company: 'L&T Finance',
    title: 'Manager Customer Service',
    dates: 'Sept 2022 - Dec 2024',
    bullets: [
      'Led a team of 130+ service professionals across 11 lines of business',
      'Tracked KPIs: FCR, AHT, CCAT, NPS, Retention',
      'Fulfilled internal & external audit requirements; fixed workflow gaps via digital solutions',
    ],
  },
  {
    company: 'IDFC FIRST Bank',
    title: 'Team Leader',
    dates: 'Sept 2019 - Sept 2022',
    bullets: [
      'Led a team of 18-20 professionals delivering personalized video banking service to HNI clients',
      'Drove cross-sells across CASA, Credit Card, Loan, MF & Insurance',
      'Expertise across 35+ banking products',
    ],
  },
  {
    company: 'Ultimate Hikers, Trekking & Adventurous Club',
    title: 'Trek Leader (volunteer)',
    dates: 'Jun 2014 - Present',
    bullets: [
      'Leads treks, instructs and guides participants, ensures logistics and safety',
      'Storytelling and survival skills across jungle trail routes',
    ],
  },
  {
    company: 'Ican BPO (USA)',
    title: 'Customer Service Executive',
    dates: 'Oct 2013 - May 2014',
    bullets: ['Generated sales through service offers; remote software troubleshooting'],
  },
  {
    company: 'Reliance Communication',
    title: 'Relationship Manager',
    dates: 'May 2012 - May 2013',
    bullets: ['Handled HNI clients & vendors; cross-sold subscriptions'],
  },
  {
    company: 'Kall Assist Solution (UK)',
    title: 'Debt Consolidator',
    dates: 'Apr 2011 - Apr 2012',
    bullets: ['Generated and qualified leads through cold calling'],
  },
  {
    company: 'Andromeda Pvt Ltd',
    title: 'Tele Marketing Executive',
    dates: 'Jun 2010 - Mar 2011',
    bullets: ['Cold-called credit card holders to generate leads; created targeted call scripts'],
  },
]

export const education = [
  "MBA, Suresh Gyan Vihar University, Jaipur (Jun 2021 - Jun 2023, CGPA 7.8)",
  "B.Com, K.G. Joshi & N.G. Bedekar College of Commerce, Thane (2018)",
  "HSC, Sushiladevi Deshmukh Mahavidyalaya, Latur (2010)",
  "SSC, Sankar Wardhini Vidyalay, Latur (2007)",
]

export const certifications = [
  'Start-Up Management Skills',
  'PMP Training Certification Course',
  'Certificate in Lean Management',
  'Data Science with Python (pursuing)',
  'PMP Exam (pursuing)',
  'Six Sigma Green Belt (pursuing)',
]

export const achievements = [
  'Raised service levels by 21% to hit 96%, improving CSAT',
  'Cut repeat calls from 33% to 17% via cross-training and IVR optimization',
  'Reduced resolution time by 26% across 38 workflow fixes; authored 58 SOPs',
  'Managed billing/service for 8+ vendors with zero audit discrepancies',
  'Lifted home loan retention from 49% to 76%; cut attrition from 11.2% to 5.8%',
]

export const skills = [
  'Customer Service Delivery', 'Operational Excellence', 'Stakeholder Management',
  'Transformational Leadership', 'Strategic Planning & Execution', 'Performance Metrics & KPI Tracking',
  'Compliance Management', 'Vendor & Billing Management', 'Digital Transformation',
  'Call Centre Technology', 'CRM Development', 'Cross-selling Strategies', 'Customer Journey Mapping',
  'Retention Strategy', 'Revenue Growth', 'Process Optimization', 'BRD Development',
  'Data Analytics & Automation', 'Power BI', 'Excel', 'PMP', 'SSGB',
]
