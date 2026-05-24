import { BookOpen, ClipboardList, Plus, Trash2, Users } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";
import ConfirmDialog from "../components/ConfirmDialog";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import PageHeader from "../components/PageHeader";

const emptyCourse = { title: "", description: "" };
const emptyTopic = { course: "", title: "", description: "", order: 1 };
const emptyLesson = { topic: "", title: "", content: "", lesson_type: "beginner", order: 1 };
const emptyTest = { course: "", title: "", description: "", time_limit: 30, is_active: true };
const emptyQuestion = {
  test: "",
  topic: "",
  text: "",
  difficulty: "easy",
  options: ["", "", "", ""],
  correctIndex: 0,
};

export default function TeacherDashboard() {
  const [courses, setCourses] = useState([]);
  const [students, setStudents] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [tests, setTests] = useState([]);
  const [courseForm, setCourseForm] = useState(emptyCourse);
  const [editingCourseId, setEditingCourseId] = useState("");
  const [topicForm, setTopicForm] = useState(emptyTopic);
  const [lessonForm, setLessonForm] = useState(emptyLesson);
  const [testForm, setTestForm] = useState(emptyTest);
  const [questionForm, setQuestionForm] = useState(emptyQuestion);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const topics = useMemo(() => courses.flatMap((course) => course.topics || []), [courses]);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [coursesRes, studentsRes, attemptsRes, testsRes] = await Promise.all([
        api.get("/courses/"),
        api.get("/users/students/"),
        api.get("/attempts/"),
        api.get("/tests/"),
      ]);
      setCourses(coursesRes.data);
      setStudents(studentsRes.data);
      setAttempts(attemptsRes.data);
      setTests(testsRes.data);
    } catch {
      setError("Мугалим панелин жүктөөдө ката кетти.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const saveCourse = async (event) => {
    event.preventDefault();
    if (editingCourseId) {
      await api.patch(`/courses/${editingCourseId}/`, courseForm);
    } else {
      await api.post("/courses/", courseForm);
    }
    setCourseForm(emptyCourse);
    setEditingCourseId("");
    load();
  };

  const editCourse = (course) => {
    setEditingCourseId(course.id);
    setCourseForm({ title: course.title, description: course.description });
  };

  const deleteCourse = async () => {
    await api.delete(`/courses/${confirmDelete.id}/`);
    setConfirmDelete(null);
    load();
  };

  const createTopic = async (event) => {
    event.preventDefault();
    await api.post("/topics/", topicForm);
    setTopicForm(emptyTopic);
    load();
  };

  const createLesson = async (event) => {
    event.preventDefault();
    await api.post("/lessons/", lessonForm);
    setLessonForm(emptyLesson);
    load();
  };

  const createTest = async (event) => {
    event.preventDefault();
    await api.post("/tests/", testForm);
    setTestForm(emptyTest);
    load();
  };

  const createQuestion = async (event) => {
    event.preventDefault();
    const { options, correctIndex, ...questionPayload } = questionForm;
    const { data: question } = await api.post("/questions/", questionPayload);
    await Promise.all(options.filter(Boolean).map((text, index) => api.post("/answer-options/", {
      question: question.id,
      text,
      is_correct: index === Number(correctIndex),
    })));
    setQuestionForm(emptyQuestion);
    load();
  };

  if (loading) {
    return <LoadingState />;
  }
  if (error) {
    return <ErrorState message={error} onRetry={load} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Мугалим панели" description="Курстарды, темаларды, сабактарды жана тесттерди башкаруу." />
      <div className="grid gap-4 md:grid-cols-3">
        <Metric icon={<BookOpen className="h-6 w-6 text-primary" />} label="Курстар" value={courses.length} />
        <Metric icon={<Users className="h-6 w-6 text-emerald-600" />} label="Окуучулар" value={students.length} />
        <Metric icon={<ClipboardList className="h-6 w-6 text-accent" />} label="Тест аракеттери" value={attempts.length} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel">
          <h2 className="text-xl font-semibold">Курс түзүү/өзгөртүү</h2>
          <form onSubmit={saveCourse} className="mt-4 space-y-3">
            <input className="input" placeholder="Курстун аталышы" value={courseForm.title} onChange={(e) => setCourseForm({ ...courseForm, title: e.target.value })} required />
            <textarea className="input min-h-24" placeholder="Сүрөттөмө" value={courseForm.description} onChange={(e) => setCourseForm({ ...courseForm, description: e.target.value })} required />
            <button className="btn-primary" type="submit"><Plus className="h-4 w-4" /> {editingCourseId ? "Сактоо" : "Курс түзүү"}</button>
          </form>
          <div className="mt-5 space-y-3">
            {courses.map((course) => (
              <div key={course.id} className="flex items-start justify-between gap-3 rounded-lg border border-slate-200 p-3">
                <Link to={`/courses/${course.id}`} className="min-w-0">
                  <p className="font-semibold">{course.title}</p>
                  <p className="text-sm text-slate-600">Темалар: {course.topics?.length || 0}</p>
                </Link>
                <div className="flex gap-2">
                  <button className="btn-secondary" type="button" onClick={() => editCourse(course)}>Edit</button>
                  <button className="btn-secondary" type="button" onClick={() => setConfirmDelete(course)} title="Delete"><Trash2 className="h-4 w-4" /></button>
                </div>
              </div>
            ))}
            {!courses.length && <EmptyState title="Курс жок" text="Биринчи курсту түзүңүз." />}
          </div>
        </section>

        <section className="panel">
          <h2 className="text-xl font-semibold">Тема жана сабак кошуу</h2>
          <form onSubmit={createTopic} className="mt-4 grid gap-3">
            <Select value={topicForm.course} onChange={(course) => setTopicForm({ ...topicForm, course })} options={courses.map((course) => ({ value: course.id, label: course.title }))} placeholder="Курс тандаңыз" />
            <input className="input" placeholder="Теманын аталышы" value={topicForm.title} onChange={(e) => setTopicForm({ ...topicForm, title: e.target.value })} required />
            <input className="input" placeholder="Кыска сүрөттөмө" value={topicForm.description} onChange={(e) => setTopicForm({ ...topicForm, description: e.target.value })} />
            <button className="btn-primary" type="submit">Тема түзүү</button>
          </form>
          <form onSubmit={createLesson} className="mt-6 grid gap-3 border-t border-slate-200 pt-4">
            <Select value={lessonForm.topic} onChange={(topic) => setLessonForm({ ...lessonForm, topic })} options={topics.map((topic) => ({ value: topic.id, label: topic.title }))} placeholder="Тема тандаңыз" />
            <input className="input" placeholder="Сабактын аталышы" value={lessonForm.title} onChange={(e) => setLessonForm({ ...lessonForm, title: e.target.value })} required />
            <textarea className="input min-h-24" placeholder="Сабак мазмуну" value={lessonForm.content} onChange={(e) => setLessonForm({ ...lessonForm, content: e.target.value })} required />
            <select className="input" value={lessonForm.lesson_type} onChange={(e) => setLessonForm({ ...lessonForm, lesson_type: e.target.value })}>
              <option value="beginner">beginner</option>
              <option value="reinforcement">reinforcement</option>
              <option value="advanced">advanced</option>
            </select>
            <button className="btn-primary" type="submit">Сабак түзүү</button>
          </form>
        </section>
      </div>

      <section className="panel">
        <h2 className="text-xl font-semibold">Тест, суроо жана жооп варианттары</h2>
        <div className="mt-4 grid gap-6 lg:grid-cols-2">
          <form onSubmit={createTest} className="grid gap-3">
            <Select value={testForm.course} onChange={(course) => setTestForm({ ...testForm, course })} options={courses.map((course) => ({ value: course.id, label: course.title }))} placeholder="Курс тандаңыз" />
            <input className="input" placeholder="Тест аталышы" value={testForm.title} onChange={(e) => setTestForm({ ...testForm, title: e.target.value })} required />
            <input className="input" placeholder="Сүрөттөмө" value={testForm.description} onChange={(e) => setTestForm({ ...testForm, description: e.target.value })} />
            <input className="input" type="number" min="1" value={testForm.time_limit} onChange={(e) => setTestForm({ ...testForm, time_limit: Number(e.target.value) })} />
            <button className="btn-primary" type="submit">Тест түзүү</button>
          </form>
          <form onSubmit={createQuestion} className="grid gap-3">
            <Select value={questionForm.test} onChange={(test) => setQuestionForm({ ...questionForm, test })} options={tests.map((test) => ({ value: test.id, label: test.title }))} placeholder="Тест тандаңыз" />
            <Select value={questionForm.topic} onChange={(topic) => setQuestionForm({ ...questionForm, topic })} options={topics.map((topic) => ({ value: topic.id, label: topic.title }))} placeholder="Тема тандаңыз" />
            <textarea className="input min-h-20" placeholder="Суроо тексти" value={questionForm.text} onChange={(e) => setQuestionForm({ ...questionForm, text: e.target.value })} required />
            {questionForm.options.map((option, index) => (
              <div key={index} className="flex gap-2">
                <input className="input" placeholder={`Вариант ${index + 1}`} value={option} onChange={(e) => {
                  const next = [...questionForm.options];
                  next[index] = e.target.value;
                  setQuestionForm({ ...questionForm, options: next });
                }} required />
                <input type="radio" name="correct" checked={Number(questionForm.correctIndex) === index} onChange={() => setQuestionForm({ ...questionForm, correctIndex: index })} />
              </div>
            ))}
            <button className="btn-primary" type="submit">Суроо кошуу</button>
          </form>
        </div>
      </section>

      <ConfirmDialog
        open={Boolean(confirmDelete)}
        title="Курсту өчүрүү"
        message={`${confirmDelete?.title || ""} курсун өчүрөсүзбү?`}
        onCancel={() => setConfirmDelete(null)}
        onConfirm={deleteCourse}
      />
    </div>
  );
}

function Metric({ icon, label, value }) {
  return <div className="panel">{icon}<p className="mt-3 text-sm text-slate-500">{label}</p><p className="text-3xl font-bold">{value}</p></div>;
}

function Select({ value, onChange, options, placeholder }) {
  return (
    <select className="input" value={value} onChange={(e) => onChange(e.target.value)} required>
      <option value="">{placeholder}</option>
      {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
    </select>
  );
}
