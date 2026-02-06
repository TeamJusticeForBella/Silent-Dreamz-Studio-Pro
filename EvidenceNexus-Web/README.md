# EvidenceNexus Web

**Secure Evidence Management for Legal Professionals**

Web-based companion to the EvidenceNexus iOS app. Built with Next.js 14, TypeScript, and Tailwind CSS.

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your Supabase credentials

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

---

## 📦 Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your GitHub repository
5. Configure:
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
6. Add Environment Variables (see below)
7. Click "Deploy"

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

---

## 🔐 Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Security
ENCRYPTION_KEY=your_32_char_key
JWT_SECRET=your_jwt_secret

# App Config
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

---

## ✅ What's Complete

✅ Next.js 14 with App Router
✅ TypeScript configuration
✅ Tailwind CSS styling
✅ Responsive landing page
✅ Dashboard interface
✅ Evidence library grid
✅ Navigation system
✅ Dark mode support

---

## 🚧 What's Next

To complete the full deployment:

### 1. Set Up Supabase (Free Tier)

```bash
# Go to supabase.com
# Create new project
# Copy your project URL and API keys
# Add them to Vercel environment variables
```

### 2. Database Schema

```sql
-- Run this in Supabase SQL Editor

create table evidence (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users not null,
  title text not null,
  description text,
  type text not null,
  date timestamptz not null,
  tags text[],
  file_url text,
  created_at timestamptz default now()
);

create table patterns (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users not null,
  type text not null,
  confidence float,
  evidence_ids uuid[],
  created_at timestamptz default now()
);
```

### 3. Enable Authentication

- Go to Supabase → Authentication → Providers
- Enable Email/Password
- Configure email templates

### 4. Storage Setup

- Go to Supabase → Storage
- Create bucket: `evidence-files`
- Set policies for authenticated users

---

## 🎯 Features

### Core Features
- 📁 Evidence library with grid/list views
- 🔍 Full-text search
- 📊 Timeline visualization
- 🚨 Pattern detection flags
- 📤 Import from multiple sources
- 🔐 Secure authentication

### Security
- AES-256 encryption
- Secure file storage
- Audit logging
- SHA-256 hashing

### AI Features (Coming Soon)
- Pattern detection engine
- OCR text extraction
- Sentiment analysis
- Timeline anomaly detection

---

## 📱 iOS + Web

This web app complements the iOS app:

- **iOS App**: Native, on-device AI, Face ID, offline support
- **Web App**: Browser access, team collaboration, cloud sync

Both share the same backend (Supabase) for seamless sync.

---

## 🛠 Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **Storage**: Supabase Storage
- **Deployment**: Vercel
- **Icons**: Lucide React

---

## 📖 Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vercel Docs](https://vercel.com/docs)

---

## 🤝 Support

Built for **Team Justice For Bella**

For Justice. For Bella. 🤍

---

## 📄 License

Proprietary - Team Justice For Bella
