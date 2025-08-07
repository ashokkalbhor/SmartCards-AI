import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowLeft, Mail, Phone, MapPin, Linkedin, CreditCard, Award, Briefcase, Code, Database, Cloud, Shield } from 'lucide-react';

const AboutPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Navigation */}
      <nav className="px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <CreditCard className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">UNGI SmartCards AI</span>
          </div>
          <Link
            to="/"
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Home</span>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              About <span className="text-primary-600 dark:text-primary-400">SmartCards AI</span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
              Empowering users to optimize their credit card usage through intelligent AI-driven recommendations
            </p>
          </motion.div>
        </div>
      </section>

      {/* Team Section */}
      <section className="px-6 py-20 bg-white dark:bg-gray-800">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-16"
            {...({} as any)}
          >
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Meet Our Team
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              The minds behind SmartCards AI
            </p>
          </motion.div>

          {/* Team Member */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-gray-700 dark:to-gray-800 rounded-2xl p-8 md:p-12"
            {...({} as any)}
          >
            <div className="grid md:grid-cols-3 gap-8 items-start">
              {/* Profile Section */}
              <div className="text-center md:text-left">
                <div className="w-32 h-32 rounded-full overflow-hidden mx-auto md:mx-0 mb-6 border-4 border-primary-600 shadow-lg">
                  <img 
                    src="/ashok-profile.jpg" 
                    alt="Ashok Kumar Kalbhor" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Ashok Kumar Kalbhor
                </h3>
                <p className="text-lg text-primary-600 dark:text-primary-400 mb-4">
                  Senior Consultant | Enterprise Architect
                </p>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  Gen AI • RPA • Full Stack • Data Engineering
                </p>
                
                {/* Contact Info */}
                <div className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-4 w-4" />
                    <span>Bengaluru</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4" />
                    <span>ashokkalbhor@gmail.com</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Phone className="h-4 w-4" />
                    <span>+91 90080 90856</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Linkedin className="h-4 w-4" />
                    <a 
                      href="https://www.linkedin.com/in/ashok-kumar-kalbhor/" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                    >
                      LinkedIn Profile
                    </a>
                  </div>
                </div>
              </div>

              {/* Professional Summary */}
              <div className="md:col-span-2">
                <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  Professional Summary
                </h4>
                <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                  Enterprise Solution Architect with 12+ years of experience across BFSI and Life Sciences domains. 
                  Currently leading the design and delivery of multi-agent Generative AI solutions leveraging GPT-4, 
                  LangChain, Azure OpenAI, and LangGraph. Proven expertise in LLMOps, containerized AI workflows, 
                  and domain-specific LLM fine-tuning. Strong background in RPA and data engineering with 
                  certifications in OCI GenAI, Data Science, and PSPO. Passionate about building ethical AI systems 
                  and empowering teams through architectural mentorship and strategic alignment.
                </p>

                {/* Technical Skills */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h5 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                      <Code className="h-5 w-5 mr-2 text-primary-600" />
                      Technical Skills
                    </h5>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                      <li>• Gen AI & LLMs: GPT-4, GPT-4o, LangChain, LangGraph, Llama 3, Claude</li>
                      <li>• LLMOps & Infra: Azure OpenAI, Vector DBs (FAISS, Qdrant), Prompt Engineering</li>
                      <li>• Cloud & DevOps: Azure, AWS, Azure DevOps, Docker, Kubernetes</li>
                      <li>• Programming: Python, SQL, C#, FastAPI, Streamlit, UiPath</li>
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                      <Award className="h-5 w-5 mr-2 text-primary-600" />
                      Certifications
                    </h5>
                    <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                      <li>• Professional Scrum Product Owner™ (PSPO 1)</li>
                      <li>• OCI Gen AI Professional (IZO-1127-24)</li>
                      <li>• OCI Data Science Professional (1Z0-1110-24)</li>
                      <li>• OCI Fusion Data Intelligence Implementation Professional</li>
                      <li>• Advance UiPath Developer</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Project Section */}
      <section className="px-6 py-20">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-center mb-16"
            {...({} as any)}
          >
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              About SmartCards AI
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Our mission to revolutionize credit card optimization
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg"
            {...({} as any)}
          >
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  Project Overview
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                  SmartCards AI is an LLM-powered intelligent agent designed to help users optimize their credit card 
                  usage by analyzing card terms, usage history, and spending context. The platform provides real-time 
                  recommendations on the best credit card to use for a given spend category and maximizes rewards using Gen AI.
                </p>
                
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  Key Features
                </h4>
                <ul className="space-y-2 text-gray-600 dark:text-gray-300">
                  <li>• Upload and store all your credit cards securely</li>
                  <li>• Ask questions like: "Which card should I use for fuel today?"</li>
                  <li>• Personalized reminders and alerts based on card benefits and expiry</li>
                  <li>• AI-powered recommendations for maximum rewards</li>
                </ul>
              </div>

              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  Tech Stack
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-primary-600 rounded-full"></div>
                    <span className="text-gray-600 dark:text-gray-300">Frontend/UI: React with TypeScript</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-600 dark:text-gray-300">Backend: FastAPI (Python)</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-green-600 rounded-full"></div>
                    <span className="text-gray-600 dark:text-gray-300">Database: PostgreSQL</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-600 dark:text-gray-300">AI Stack: GPT-4o, LangChain agents, FAISS</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-orange-600 rounded-full"></div>
                    <span className="text-gray-600 dark:text-gray-300">Infra: Dockerized containers, Vector DB</span>
                  </div>
                </div>

                <div className="mt-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <h4 className="font-semibold text-primary-600 dark:text-primary-400 mb-2">
                    LLM Capabilities
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    PDF ingestion of card benefits, RAG architecture for accurate retrieval, 
                    context-aware prompt construction for personalized recommendations.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 bg-primary-600 dark:bg-primary-700">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Optimize Your Credit Cards?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join users who are already maximizing their credit card rewards with SmartCards AI.
            </p>
            <Link
              to="/register"
              className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-4 rounded-lg text-lg font-semibold transition-colors inline-flex items-center space-x-2"
            >
              <span>Get Started Free</span>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <CreditCard className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold">UNGI SmartCards AI</span>
            </div>
            <div className="flex items-center space-x-6">
              <Link
                to="/about"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                About Us
              </Link>
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                Privacy Policy
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                Terms of Service
              </a>
              <div className="text-gray-400 text-sm">
                © 2025 UNGI SmartCards AI. Every swipe, Optimized.
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AboutPage; 