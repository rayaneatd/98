# Ninety Eight Percent (98%) - Project Specification

## 1. Overview
Ninety Eight Percent is an intensive tech learning application built with Python and Flet. Unlike traditional e-learning platforms where self-pacing often leads to dropouts, this platform enforces accountability. It pairs the learner with a strict, personal AI coach that plans a tailored roadmap, tracks adherence, demands written justifications for missed milestones, and adapts coursework dynamically until a final proctored-style examination.

---

# 2. Core User Journey

### 2.1 Authentication
- Users sign in using Google authentication.
- A user profile is initialized to persist onboarding preferences, progress, strikes, and exam records.

### 2.2 Onboarding Workflow
The onboarding sequence collects critical data points to shape the learner's curriculum:
1. **Skill Selection & Motivation**:
   - Learners can select multiple skills (e.g., Python + SQL), either independently or as combined career tracks.
   - Learners must state explicitly *why* they want to learn these technologies. This rationale is used later by the AI coach to reinforce motivation during slumps.
2. **Background & Current Level**:
   - Educational or professional background.
   - Self-assessed baseline (absolute beginner, intermediate, switching careers, etc.).
3. **Schedule & Real Availability**:
   - Dedicated hours per week and preferred daily time slots.
   - Specific schedule constraints or blackout periods.
4. **Target Deadline & Mastery Level**:
   - Target completion date.
   - Expected proficiency level (e.g., job-ready junior, project-specific mastery).

---

# 3. The Personal AI Coach

### 3.1 Curriculum Generation
- The AI coach generates a customized, granular study program mapped against the learner's schedule and chosen deadline.
- Lessons balance conceptual understanding, practical exercises, and progressive projects.

### 3.2 Attendance, Missed Sessions, and the "Excuse System"
- The coach tracks deadlines and scheduled sessions.
- If a learner misses sessions without prior notice, access to subsequent material is locked.
- To unlock the curriculum, the learner must submit a written explanation directly to the AI coach.
- The AI evaluates the submitted excuse:
  - **Convincing (Valid Emergency / Legitimate Blocker)**: The absence is pardoned, streaks remain intact, and the schedule is recalibrated.
  - **Moderately Convincing**: A penalty is applied based on the learner's past absence record (e.g., warning, makeup assignment).
  - **Unconvincing (Procrastination, poor excuses)**: The excuse is rejected. A direct penalty is enforced (additional drill assignments, reduced grace periods).

### 3.3 Resource Curation & Unblocking
- For foundational topics, the coach curates high-quality free external resources (such as targeted YouTube setup tutorials and documentation).
- If external materials do not resolve the learner's problem, the coach enters an interactive mode to explain concepts and guide the learner past blockers without giving away direct answers.

---

# 4. Adaptive Learning & Assignments
- As the learner progresses through the track, assignments and projects scale in difficulty.
- Future course modules automatically adapt: topics mastered quickly are condensed, while topics showing friction receive additional practice drills.

---

# 5. Final Certification Exam
- At the agreed deadline, the learner unlocks the final exam.
- The exam follows a strict, formal testing environment (similar to Pearson VUE standards):
  - Timed testing session.
  - Mixed assessment format (theoretical questions and hands-on coding challenges).
  - Passing threshold: minimum 70 / 100.
- Achieving 70% or higher generates a verifiable completion certificate issued in the learner's full name.

---

# 6. Social & Collaborative Features (Coming Soon)
- **Study Groups**: Grouping learners with matching tracks and deadlines to study collaboratively.
- **Peer Presentations**: Scheduled presentation slots where learners explain technical concepts or showcase their project implementations to peers.
- These features are displayed in the application interface as "Coming Soon".

---

# 7. Technical Foundation
- **UI Framework**: Flet (Python desktop/cross-platform engine).
- **Package & Environment Management**: `uv`.
- **Backend Logic**: Pure Python services for AI interaction, state management, local database persistence, and certificate generation.
