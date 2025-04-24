import React, { useState } from 'react';
import { FileSpreadsheet, Plus, CheckCircle, Users, BarChart3, Database, Share2, Lock } from 'lucide-react';
import clsx from 'clsx';

interface LandingPageProps {
  onCreateSpreadsheet: (name: string) => void;
}

const features = [
  {
    title: "Real-time Collaboration",
    description: "Work together with your team in real-time, seeing changes as they happen.",
    icon: <Users className="h-6 w-6 text-emerald-500" />,
  },
  {
    title: "Advanced Formulas",
    description: "Powerful formula capabilities to analyze and manipulate your data effectively.",
    icon: <BarChart3 className="h-6 w-6 text-emerald-500" />,
  },
  {
    title: "Data Visualization",
    description: "Create beautiful charts and graphs to visualize your data and gain insights.",
    icon: <BarChart3 className="h-6 w-6 text-emerald-500" />,
  },
  {
    title: "Cloud Storage",
    description: "Access your spreadsheets from anywhere with secure cloud storage.",
    icon: <Database className="h-6 w-6 text-emerald-500" />,
  },
  {
    title: "Sharing & Permissions",
    description: "Control who can view and edit your spreadsheets with granular permissions.",
    icon: <Share2 className="h-6 w-6 text-emerald-500" />,
  },
  {
    title: "Data Security",
    description: "Enterprise-grade security to keep your sensitive data protected.",
    icon: <Lock className="h-6 w-6 text-emerald-500" />,
  },
];

const testimonials = [
  {
    content: "SpreadHub has transformed how our team manages data. The collaboration features are seamless and intuitive.",
    name: "Sarah Johnson",
    role: "Product Manager at TechCorp",
    image: "https://images.pexels.com/photos/3796217/pexels-photo-3796217.jpeg?auto=compress&cs=tinysrgb&w=100",
  },
  {
    content: "We switched from Excel to SpreadHub and haven't looked back. It's faster, more collaborative, and just works better.",
    name: "Michael Chen",
    role: "Data Analyst at FinanceIQ",
    image: "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=100",
  },
  {
    content: "The formula capabilities in SpreadHub are incredible. We're able to build complex models with ease.",
    name: "Jessica Williams",
    role: "Financial Consultant",
    image: "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=100",
  },
];

const LandingPage: React.FC<LandingPageProps> = ({ onCreateSpreadsheet }) => {
  const [isCreating, setIsCreating] = useState(false);
  const [newSpreadsheetName, setNewSpreadsheetName] = useState('');

  const handleCreate = () => {
    if (newSpreadsheetName.trim()) {
      onCreateSpreadsheet(newSpreadsheetName.trim());
    } else {
      onCreateSpreadsheet('Untitled Spreadsheet');
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-white">
      <header className="sticky top-0 z-40 border-b bg-white">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="h-6 w-6 text-emerald-500" />
            <span className="text-xl font-bold">SpreadHub</span>
          </div>
          <nav className="hidden md:flex gap-6">
            <a href="#features" className="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900">
              Features
            </a>
            <a href="#testimonials" className="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900">
              Testimonials
            </a>
          </nav>
          <button
            onClick={() => setIsCreating(true)}
            className="flex items-center gap-2 rounded-full bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-all hover:bg-emerald-700"
          >
            Get Started
          </button>
        </div>
      </header>

      <main className="flex-1">
        <section className="relative overflow-hidden bg-white py-20 sm:py-32">
          <div className="container mx-auto px-4">
            <div className="grid gap-12 lg:grid-cols-2 lg:gap-8">
              <div className="flex flex-col justify-center">
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
                  Create, collaborate, and analyze spreadsheets with ease
                </h1>
                <p className="mt-4 text-lg text-gray-600 sm:mt-6">
                  A powerful spreadsheet application that helps you organize data, collaborate with your team, and make
                  better decisions.
                </p>
                <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:gap-4">
                  <button
                    onClick={() => setIsCreating(true)}
                    className="flex items-center justify-center gap-2 rounded-full bg-emerald-600 px-6 py-3 text-sm font-medium text-white transition-all hover:bg-emerald-700"
                  >
                    Try for free
                  </button>
                  <button className="flex items-center justify-center gap-2 rounded-full border border-gray-300 px-6 py-3 text-sm font-medium text-gray-700 transition-all hover:bg-gray-50">
                    See how it works
                  </button>
                </div>
                <div className="mt-6 flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-emerald-500" />
                  <span className="text-sm text-gray-600">No credit card required</span>
                </div>
              </div>
              <div className="relative">
                <div className="aspect-[4/3] overflow-hidden rounded-2xl bg-gray-50">
                  <img
                    src="https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                    alt="Team collaboration"
                    className="h-full w-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="bg-gray-50 py-20 sm:py-32">
          <div className="container mx-auto px-4">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Powerful features for your data needs
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Everything you need to manage, analyze, and share your data effectively
              </p>
            </div>
            <div className="mx-auto mt-16 grid max-w-5xl gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {features.map((feature) => (
                <div
                  key={feature.title}
                  className="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:shadow-md"
                >
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50">
                    {feature.icon}
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-gray-600">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="testimonials" className="bg-white py-20 sm:py-32">
          <div className="container mx-auto px-4">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Loved by teams worldwide
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                See what our customers have to say about SpreadHub
              </p>
            </div>
            <div className="mx-auto mt-16 grid max-w-5xl gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {testimonials.map((testimonial) => (
                <div
                  key={testimonial.name}
                  className="flex flex-col justify-between rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
                >
                  <p className="text-gray-600">{testimonial.content}</p>
                  <div className="mt-6 flex items-center gap-4">
                    <img
                      src={testimonial.image}
                      alt={testimonial.name}
                      className="h-10 w-10 rounded-full object-cover"
                    />
                    <div>
                      <div className="font-medium text-gray-900">{testimonial.name}</div>
                      <div className="text-sm text-gray-600">{testimonial.role}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-emerald-50 py-20 sm:py-32">
          <div className="container mx-auto px-4">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Ready to get started?
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Join thousands of teams who are already using SpreadHub to manage their data.
              </p>
              <button
                onClick={() => setIsCreating(true)}
                className="mt-8 flex items-center gap-2 rounded-full bg-emerald-600 px-6 py-3 text-sm font-medium text-white transition-all hover:bg-emerald-700 mx-auto"
              >
                Start your free trial
              </button>
              <p className="mt-4 text-sm text-gray-600">No credit card required</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t bg-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileSpreadsheet className="h-5 w-5 text-emerald-500" />
              <span className="font-bold">SpreadHub</span>
            </div>
            <p className="text-sm text-gray-600">
              © {new Date().getFullYear()} SpreadHub. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      {isCreating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="w-full max-w-lg rounded-2xl bg-white p-8">
            <h2 className="text-2xl font-bold text-gray-900">Create New Spreadsheet</h2>
            <input
              type="text"
              className="mt-6 w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 outline-none transition-all focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100"
              placeholder="Untitled Spreadsheet"
              value={newSpreadsheetName}
              onChange={(e) => setNewSpreadsheetName(e.target.value)}
              autoFocus
            />
            <div className="mt-8 flex justify-end gap-4">
              <button
                className="rounded-lg px-4 py-2 text-gray-700 hover:bg-gray-100"
                onClick={() => setIsCreating(false)}
              >
                Cancel
              </button>
              <button
                className="rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white shadow-sm transition-all hover:bg-emerald-700"
                onClick={handleCreate}
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;