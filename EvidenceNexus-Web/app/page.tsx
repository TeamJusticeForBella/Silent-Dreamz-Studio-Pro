import Link from 'next/link'
import { Shield, Lock, Cloud, Zap, FileText, Users } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <Shield className="w-20 h-20 text-blue-600" />
            </div>

            <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
              EvidenceNexus
            </h1>

            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Secure, Private, Professional Evidence Management
            </p>

            <p className="text-lg text-gray-500 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
              Built for high-stakes legal cases. Military-grade encryption, on-device processing,
              and AI-powered pattern detection. For Justice. For Bella. 🤍
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/auth/signin"
                className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold"
              >
                Get Started
              </Link>
              <Link
                href="/dashboard"
                className="px-8 py-4 bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors text-lg font-semibold border-2 border-blue-600"
              >
                View Demo
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h2 className="text-4xl font-bold text-center mb-16">
          Professional-Grade Features
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Lock className="w-12 h-12 text-blue-600" />}
            title="Military-Grade Security"
            description="AES-256 encryption, secure authentication, and tamper-evident audit logs protect your sensitive evidence."
          />

          <FeatureCard
            icon={<Cloud className="w-12 h-12 text-purple-600" />}
            title="Private & Secure"
            description="Your data stays encrypted at rest and in transit. Optional on-device processing for maximum privacy."
          />

          <FeatureCard
            icon={<Zap className="w-12 h-12 text-yellow-600" />}
            title="AI-Powered Analysis"
            description="Automatic pattern detection, timeline analysis, and evidence categorization using advanced AI."
          />

          <FeatureCard
            icon={<FileText className="w-12 h-12 text-green-600" />}
            title="Multi-Source Import"
            description="Import from Gmail, Outlook, social media, photos, documents, and voice recordings."
          />

          <FeatureCard
            icon={<Users className="w-12 h-12 text-red-600" />}
            title="Collaboration Ready"
            description="Share evidence securely with your legal team while maintaining chain of custody."
          />

          <FeatureCard
            icon={<Shield className="w-12 h-12 text-indigo-600" />}
            title="Legal Integrity"
            description="SHA-256 hashing, immutable timestamps, and comprehensive audit trails for court admissibility."
          />
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-16">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Secure Your Evidence?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join legal professionals using EvidenceNexus to manage sensitive case materials.
          </p>
          <Link
            href="/auth/signin"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition-colors text-lg font-semibold"
          >
            Start Free Trial
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-bold mb-4">EvidenceNexus</h3>
              <p className="text-gray-400">
                Professional evidence management for legal professionals.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white">Terms of Service</Link></li>
                <li><Link href="/security" className="hover:text-white">Security</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">Contact</h3>
              <p className="text-gray-400">
                For Justice. For Bella. 🤍
              </p>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
            <p>© 2026 Team Justice For Bella. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}

function FeatureCard({ icon, title, description }: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-2 dark:text-white">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{description}</p>
    </div>
  )
}
