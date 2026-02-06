'use client'

import { useState } from 'react'
import {
  FileText,
  Image as ImageIcon,
  Video,
  Mic,
  Mail,
  AlertTriangle,
  Calendar,
  TrendingUp,
  Upload,
  Search,
  Filter
} from 'lucide-react'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('library')

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900">
      {/* Header */}
      <header className="bg-white dark:bg-slate-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              EvidenceNexus
            </h1>
            <div className="flex items-center gap-4">
              <button className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg">
                <Search className="w-5 h-5" />
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Import Evidence
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <TabButton
              active={activeTab === 'library'}
              onClick={() => setActiveTab('library')}
              icon={<FileText className="w-4 h-4" />}
            >
              Library
            </TabButton>
            <TabButton
              active={activeTab === 'timeline'}
              onClick={() => setActiveTab('timeline')}
              icon={<Calendar className="w-4 h-4" />}
            >
              Timeline
            </TabButton>
            <TabButton
              active={activeTab === 'patterns'}
              onClick={() => setActiveTab('patterns')}
              icon={<AlertTriangle className="w-4 h-4" />}
            >
              Patterns
            </TabButton>
            <TabButton
              active={activeTab === 'analytics'}
              onClick={() => setActiveTab('analytics')}
              icon={<TrendingUp className="w-4 h-4" />}
            >
              Analytics
            </TabButton>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Evidence"
            value="247"
            icon={<FileText className="w-6 h-6 text-blue-600" />}
            trend="+12 this week"
          />
          <StatCard
            title="Critical Patterns"
            value="8"
            icon={<AlertTriangle className="w-6 h-6 text-red-600" />}
            trend="3 unreviewed"
          />
          <StatCard
            title="Sources"
            value="5"
            icon={<Mail className="w-6 h-6 text-green-600" />}
            trend="Gmail, Photos"
          />
          <StatCard
            title="Storage Used"
            value="2.4 GB"
            icon={<Upload className="w-6 h-6 text-purple-600" />}
            trend="of 10 GB"
          />
        </div>

        {/* Evidence Grid */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold dark:text-white">Recent Evidence</h2>
            <button className="flex items-center gap-2 px-4 py-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg">
              <Filter className="w-4 h-4" />
              Filter
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <EvidenceCard
              title="Email Thread - Foster Care Documents"
              type="email"
              date="2026-02-05"
              tags={["Koohanim", "Obstruction"]}
              icon={<Mail className="w-8 h-8 text-blue-600" />}
            />
            <EvidenceCard
              title="Medical Records - Infection Report"
              type="document"
              date="2026-02-04"
              tags={["Medical", "Neglect"]}
              icon={<FileText className="w-8 h-8 text-green-600" />}
            />
            <EvidenceCard
              title="Voice Recording - Phone Call"
              type="audio"
              date="2026-02-03"
              tags={["Davis", "Deception"]}
              icon={<Mic className="w-8 h-8 text-purple-600" />}
            />
            <EvidenceCard
              title="Photos - Foster Home Conditions"
              type="photo"
              date="2026-02-02"
              tags={["Evidence", "Foster Neglect"]}
              icon={<ImageIcon className="w-8 h-8 text-red-600" />}
            />
            <EvidenceCard
              title="Video Deposition - Attorney Misconduct"
              type="video"
              date="2026-02-01"
              tags={["Forrey-Baker", "Misconduct"]}
              icon={<Video className="w-8 h-8 text-yellow-600" />}
            />
            <EvidenceCard
              title="Text Messages - Timeline Inconsistencies"
              type="text"
              date="2026-01-31"
              tags={["Timeline Issue", "Obstruction"]}
              icon={<FileText className="w-8 h-8 text-indigo-600" />}
            />
          </div>
        </div>
      </main>
    </div>
  )
}

function TabButton({
  active,
  onClick,
  icon,
  children
}: {
  active: boolean
  onClick: () => void
  icon: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={`
        flex items-center gap-2 px-4 py-4 border-b-2 transition-colors
        ${active
          ? 'border-blue-600 text-blue-600 dark:text-blue-400'
          : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
        }
      `}
    >
      {icon}
      {children}
    </button>
  )
}

function StatCard({
  title,
  value,
  icon,
  trend
}: {
  title: string
  value: string
  icon: React.ReactNode
  trend: string
}) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-600 dark:text-gray-400">{title}</span>
        {icon}
      </div>
      <div className="text-3xl font-bold dark:text-white mb-1">{value}</div>
      <div className="text-xs text-gray-500 dark:text-gray-400">{trend}</div>
    </div>
  )
}

function EvidenceCard({
  title,
  type,
  date,
  tags,
  icon
}: {
  title: string
  type: string
  date: string
  tags: string[]
  icon: React.ReactNode
}) {
  return (
    <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer">
      <div className="flex items-start justify-between mb-4">
        {icon}
        <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded">
          {type}
        </span>
      </div>

      <h3 className="font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
        {title}
      </h3>

      <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
        {date}
      </p>

      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span
            key={tag}
            className="text-xs px-2 py-1 bg-gray-200 dark:bg-slate-600 text-gray-700 dark:text-gray-300 rounded"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  )
}
