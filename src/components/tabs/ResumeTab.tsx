import { useState } from 'react'
import { achievements, certifications, education, jobs, skills, summary } from '../../data/resume'

export function ResumeTab() {
  const [openJob, setOpenJob] = useState<string | null>(jobs[0].company)

  return (
    <div className="tab-panel resume-tab">
      <p className="resume-summary">{summary}</p>

      <h3 className="resume-heading">Experience</h3>
      <div className="resume-accordion">
        {jobs.map((job) => {
          const isOpen = openJob === job.company
          return (
            <div key={job.company} className={`resume-job ${isOpen ? 'resume-job--open' : ''}`}>
              <button
                className="resume-job-header"
                onClick={() => setOpenJob(isOpen ? null : job.company)}
              >
                <span>
                  <strong>{job.title}</strong> — {job.company}
                </span>
                <span className="resume-job-dates">{job.dates}</span>
              </button>
              {isOpen && (
                <ul className="resume-job-bullets">
                  {job.bullets.map((bullet) => (
                    <li key={bullet}>{bullet}</li>
                  ))}
                </ul>
              )}
            </div>
          )
        })}
      </div>

      <div className="resume-grid">
        <div>
          <h3 className="resume-heading">Key Achievements</h3>
          <ul className="resume-list">
            {achievements.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="resume-heading">Education</h3>
          <ul className="resume-list">
            {education.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
          <h3 className="resume-heading">Certifications</h3>
          <ul className="resume-list">
            {certifications.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </div>
      </div>

      <h3 className="resume-heading">Skills</h3>
      <div className="resume-skills">
        {skills.map((skill) => (
          <span key={skill} className="resume-skill-pill">{skill}</span>
        ))}
      </div>
    </div>
  )
}
