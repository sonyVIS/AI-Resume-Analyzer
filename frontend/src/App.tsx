import { useState } from "react"
import "./App.css"

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const uploadResume = async () => {
    console.log("Selected file:", selectedFile)

    if (!selectedFile) {
      alert("Please select a resume first.")
      return
    }

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append("file", selectedFile)

      const response = await fetch(
        "http://127.0.0.1:8000/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      )

      const data = await response.json()

      console.log("Resume analysis:", data)
      setAnalysis(data)
    } catch (error) {
      console.error("Upload error:", error)
      alert("Unable to analyze the resume. Please check the backend.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-logo">AI</div>

          <div>
            <h2>ResumeAI</h2>
            <span>Career Intelligence</span>
          </div>
        </div>

        <nav className="navigation">

          <div className="nav-section-title">
            WORKSPACE
          </div>

          <div className="nav-item active">
            <span>⌂</span>
            Dashboard
          </div>

          <div className="nav-item">
            <span>▣</span>
            Resume Analysis
          </div>

          <div className="nav-item">
            <span>◎</span>
            Job Matching
          </div>

          <div className="nav-item">
            <span>◆</span>
            Career Paths
          </div>

          <div className="nav-section-title second">
            INSIGHTS
          </div>

          <div className="nav-item">
            <span>◈</span>
            Skills
          </div>

          <div className="nav-item">
            <span>▤</span>
            Projects
          </div>

          <div className="nav-item">
            <span>✦</span>
            Suggestions
          </div>

        </nav>

        <div className="sidebar-bottom">

          <div className="help-box">
            <div className="help-icon">?</div>

            <div>
              <strong>Need help?</strong>
              <p>Improve your resume with AI insights.</p>
            </div>
          </div>

          <div className="profile">
            <div className="profile-avatar">S</div>

            <div>
              <strong>Candidate</strong>
              <span>Resume workspace</span>
            </div>
          </div>

        </div>

      </aside>


      {/* MAIN AREA */}
      <main className="main-content">

        {/* TOP BAR */}
        <header className="topbar">

          <div>
            <span className="page-label">WORKSPACE</span>
            <h1>Dashboard</h1>
          </div>

          <div className="topbar-right">

            <div className="status">
              <span className="status-dot"></span>
              AI System Ready
            </div>

            <div className="top-avatar">
              S
            </div>

          </div>

        </header>


        {/* CONTENT */}
        <div className="dashboard">

          {/* HERO */}
          <section className="hero">

            <div className="hero-content">

              <span className="hero-badge">
                ✦ AI-POWERED CAREER INTELLIGENCE
              </span>

              <h2>
                Understand your resume.
                <br />
                <span>Discover your potential.</span>
              </h2>

              <p>
                Analyze your skills, projects and resume strength,
                then discover career paths that match your profile.
              </p>

              <div className="hero-actions">

                <label className="primary-upload">

                  <span>↑</span>
                  Upload Resume

                  <input
                    type="file"
                    accept=".pdf"
                    hidden
                    onChange={(event) => {
                      const file = event.target.files?.[0]

                      if (file) {
                        setSelectedFile(file)
                      }
                    }}
                  />

                </label>

                <button
                  className="primary-analyze"
                  onClick={uploadResume}
                  disabled={loading}
                >
                  {loading ? "Analyzing..." : "Analyze Resume →"}
                </button>

              </div>

              {selectedFile && (
                <div className="selected-file">
                  <span>📄</span>
                  <div>
                    <strong>{selectedFile.name}</strong>
                    <small>PDF resume selected</small>
                  </div>
                </div>
              )}

            </div>

            <div className="hero-visual">

              <div className="ai-orbit">
                <div className="orbit-ring ring-one"></div>
                <div className="orbit-ring ring-two"></div>

                <div className="ai-core">
                  <span>✦</span>
                  <strong>AI</strong>
                </div>

              </div>

            </div>

          </section>


          {/* STAT CARDS */}
          <section className="stats-grid">

            <div className="stat-card">

              <div className="stat-icon purple">
                ◉
              </div>

              <div>
                <span>Resume Score</span>

                <strong>
                  {analysis?.total_score ?? "--"}
                  {analysis?.total_score !== undefined && "/100"}
                </strong>

                <small>
                  {analysis
                    ? "Based on your resume"
                    : "Analyze resume to calculate"}
                </small>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon blue">
                ✦
              </div>

              <div>
                <span>Skills Detected</span>

                <strong>
                  {analysis?.skills?.length ?? "--"}
                </strong>

                <small>
                  Technical skills found
                </small>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon green">
                ▣
              </div>

              <div>
                <span>Projects</span>

                <strong>
                  {analysis?.project_count ?? "--"}
                </strong>

                <small>
                  Projects analyzed
                </small>
              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon orange">
                ◆
              </div>

              <div>
                <span>Career Paths</span>

                <strong>
                  {analysis?.top_careers?.length ?? "--"}
                </strong>

                <small>
                  Matching career paths
                </small>
              </div>

            </div>

          </section>

          {/* RESUME ANALYSIS RESULTS */}
{analysis && (
  <section className="panel" style={{ marginTop: "20px" }}>

    <div className="panel-heading">

      <div>
        <span className="panel-label">
          RESUME ANALYSIS
        </span>

        <h3>Resume insights</h3>
      </div>

      <span className="panel-badge">
        AI
      </span>

    </div>


    {/* SKILLS */}
    <div style={{ marginBottom: "22px" }}>

      <strong style={{ fontSize: "13px" }}>
        Skills detected
      </strong>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          marginTop: "10px",
        }}
      >

        {analysis.skills?.map((skill: string, index: number) => (

          <span
            key={index}
            style={{
              padding: "6px 10px",
              background: "#ede9fe",
              color: "#6d28d9",
              borderRadius: "7px",
              fontSize: "10px",
              fontWeight: 700,
            }}
          >
            {skill}
          </span>

        ))}

      </div>

    </div>


    {/* PROJECT CATEGORIES */}
    <div style={{ marginBottom: "22px" }}>

      <strong style={{ fontSize: "13px" }}>
        Project categories
      </strong>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          marginTop: "10px",
        }}
      >

        {analysis.project_categories?.map(
          (category: string, index: number) => (

            <span
              key={index}
              style={{
                padding: "6px 10px",
                background: "#dbeafe",
                color: "#1d4ed8",
                borderRadius: "7px",
                fontSize: "10px",
                fontWeight: 700,
              }}
            >
              {category}
            </span>

          )
        )}

      </div>

    </div>


    {/* SUGGESTIONS */}
    <div>

      <strong style={{ fontSize: "13px" }}>
        AI suggestions
      </strong>

      <p
        style={{
          marginTop: "8px",
          color: "#667085",
          fontSize: "11px",
          lineHeight: 1.6,
        }}
      >
        {analysis.suggestions || "No suggestions available yet."}
      </p>

    </div>

  </section>
)}


          {/* LOWER GRID */}
          <section className="dashboard-grid">

            {/* QUICK ANALYSIS */}
            <div className="panel analysis-panel">

              <div className="panel-heading">

                <div>
                  <span className="panel-label">
                    RESUME INTELLIGENCE
                  </span>

                  <h3>What we analyze</h3>
                </div>

                <span className="panel-badge">
                  AI
                </span>

              </div>


              <div className="analysis-list">

                <div className="analysis-item">
                  <div className="analysis-number">01</div>

                  <div>
                    <strong>Skills Detection</strong>
                    <p>
                      Identify technical skills from your resume.
                    </p>
                  </div>

                  <span>→</span>
                </div>


                <div className="analysis-item">
                  <div className="analysis-number">02</div>

                  <div>
                    <strong>Project Analysis</strong>
                    <p>
                      Understand project categories and experience.
                    </p>
                  </div>

                  <span>→</span>
                </div>


                <div className="analysis-item">
                  <div className="analysis-number">03</div>

                  <div>
                    <strong>Career Intelligence</strong>
                    <p>
                      Discover career paths matching your profile.
                    </p>
                  </div>

                  <span>→</span>
                </div>


                <div className="analysis-item">
                  <div className="analysis-number">04</div>

                  <div>
                    <strong>Improvement Suggestions</strong>
                    <p>
                      Get actionable ideas to strengthen your resume.
                    </p>
                  </div>

                  <span>→</span>
                </div>

              </div>

            </div>


            {/* CAREER CARD */}
            <div className="panel career-panel">

              <div className="panel-heading">

                <div>
                  <span className="panel-label">
                    CAREER INTELLIGENCE
                  </span>

                  <h3>Recommended paths</h3>
                </div>

                <span className="sparkle">✦</span>

              </div>


              {analysis?.top_careers?.length ? (

                <div className="career-list">

                  {analysis.top_careers
                    .slice(0, 3)
                    .map((career: any, index: number) => (

                      <div
                        className="career-item"
                        key={index}
                      >

                        <div className="career-rank">
                          {index + 1}
                        </div>

                        <div>
                          <strong>
                            {typeof career === "string"
                              ? career
                              : career.career}
                          </strong>

                          <span>
                            AI career recommendation
                          </span>
                        </div>

                        <span className="career-arrow">
                          →
                        </span>

                      </div>

                    ))}

                </div>

              ) : (

                <div className="empty-career">

                  <div className="empty-icon">
                    ✦
                  </div>

                  <h4>Your career insights will appear here</h4>

                  <p>
                    Upload and analyze your resume to discover
                    matching career paths.
                  </p>

                </div>

              )}

            </div>

          </section>


          {/* BOTTOM FEATURE ROW */}
          <section className="feature-row">

            <div className="mini-feature">
              <span>🎯</span>

              <div>
                <strong>Job Matching</strong>
                <p>
                  Compare your resume with job requirements.
                </p>
              </div>

              <b>→</b>
            </div>


            <div className="mini-feature">
              <span>🧠</span>

              <div>
                <strong>Skill Intelligence</strong>
                <p>
                  Understand your strongest technical skills.
                </p>
              </div>

              <b>→</b>
            </div>


            <div className="mini-feature">
              <span>💡</span>

              <div>
                <strong>Smart Suggestions</strong>
                <p>
                  Find ways to improve your resume.
                </p>
              </div>

              <b>→</b>
            </div>

          </section>

        </div>

      </main>

    </div>
  )
}

export default App