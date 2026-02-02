import PiiEditor from './components/PiiEditor';
import Dashboard from './components/Dashboard';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="flex flex-col gap-2 border-b pb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            PII Detection Service
          </h1>
          <p className="text-gray-600">
            Real-time Personally Identifiable Information (PII) detection powered by Local SLMs (Gemma).
          </p>
        </header>

        <section>
          <PiiEditor />
        </section>

        <section>
          <Dashboard />
        </section>
      </div>
    </main>
  );
}
