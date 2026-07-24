// pages/index.tsx
import { FormEvent, useState } from "react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<null | "ok" | "error">(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);

    const form = e.currentTarget;
    const data = {
      name: form.name.value,
      role: form.role.value,
      company: form.company.value,
      city: form.city.value,
      email: form.email.value,
      phone: form.phone.value,
      employees: form.employees.value,
      fleet: form.fleet.value,
      biggest_pain: form.biggest_pain.value,
      goal: form.goal.value,
    };

    try {
      const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("Failed");
      setStatus("ok");
      form.reset();
    } catch (err) {
      console.error(err);
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      {/* Your hero + sections can reuse the same layout we created earlier */}
      <section id="audit">
        <h2>Book a free 60‑minute Operations Audit</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Your name</label>
            <input name="name" required />
          </div>
          <div>
            <label>Role</label>
            <input name="role" required />
          </div>
          <div>
            <label>Company</label>
            <input name="company" required />
          </div>
          <div>
            <label>Primary corridor / city</label>
            <input name="city" />
          </div>
          <div>
            <label>Work email</label>
            <input type="email" name="email" required />
          </div>
          <div>
            <label>WhatsApp number</label>
            <input name="phone" required />
          </div>
          <div>
            <label>Team size</label>
            <select name="employees">
              <option value="">Select</option>
              <option value="under-20">Under 20</option>
              <option value="20-50">20–50</option>
              <option value="50-100">50–100</option>
              <option value="100-200">100–200</option>
              <option value="200-plus">200+</option>
            </select>
          </div>
          <div>
            <label>Fleet size (approx.)</label>
            <input name="fleet" />
          </div>
          <div>
            <label>Biggest pain point right now</label>
            <textarea name="biggest_pain" />
          </div>
          <div>
            <label>If the audit is a success, what changes in 90 days?</label>
            <textarea name="goal" />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? "Submitting..." : "Submit audit request"}
          </button>
          {status === "ok" && <p>Thanks, your request was received.</p>}
          {status === "error" && <p>Something went wrong. Please try again.</p>}
        </form>
      </section>
    </main>
  );
}
