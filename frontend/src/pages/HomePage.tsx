import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, CreditCard, TrendingUp, Shield, Zap, Bike, AlertTriangle, Lightbulb, Heart } from 'lucide-react';

const HomePage: React.FC = () => {
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
          <div className="flex items-center space-x-4">
            <Link
              to="/login"
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
              Every swipe,{' '}
              <span className="text-primary-600 dark:text-primary-400">Optimized</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              UNGI SmartCards AI uses advanced machine learning and Gen AI to recommend the perfect credit card for every purchase, maximizing your rewards and savings.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors flex items-center justify-center space-x-2"
              >
                <span>Start Optimizing</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <a
                href="https://youtu.be/mrgtCuA9jck?si=maURPUhs3m8z4hzN"
                target="_blank"
                rel="noopener noreferrer"
                className="border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 px-8 py-4 rounded-lg text-lg font-semibold transition-colors inline-block text-center"
              >
                Watch Demo
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-16"
            {...({} as any)}
          >
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose UNGI SmartCards AI?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Our Gen AI-powered platform analyzes your spending patterns and recommends the optimal card for every transaction.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-center p-6"
              {...({} as any)}
            >
              <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Smart Recommendations
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                AI analyzes your spending and suggests the best card for each purchase to maximize rewards.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-center p-6"
              {...({} as any)}
            >
              <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Maximize Rewards
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Never miss out on bonus categories, sign-up bonuses, or cashback opportunities.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="text-center p-6"
              {...({} as any)}
            >
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Secure & Private
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Bank-level security protects your data while our AI optimizes your spending strategy.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Founder Story Section */}
      <section className="px-6 py-24 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-16"
            {...({} as any)}
          >
            <span className="inline-block text-xs font-semibold uppercase tracking-widest text-primary-600 dark:text-primary-400 mb-3">The Origin Story</span>
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why I Built This
            </h2>
            <p className="text-lg text-gray-500 dark:text-gray-400">A story of a fresh graduate, a shiny new credit card, and a very expensive Pulsar 150.</p>
          </motion.div>

          {/* Story Timeline */}
          <div className="relative">
            {/* Vertical line */}
            <div className="absolute left-8 top-0 bottom-0 w-px bg-gray-200 dark:bg-gray-700 hidden md:block" />

            <div className="space-y-10">

              {/* Chapter 1 */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900 items-center justify-center z-10">
                  <CreditCard className="w-7 h-7 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                  <span className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">2013 — The Beginning</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">A salary account and a very persuasive bank salesperson</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    Fresh out of college, first job, first paycheck — and my very first bank account at Citi Bank India.
                    Before this, I was that guy borrowing his parents' ATM card for literally everything.
                    So naturally, when the bank offered me a credit card with promises of flight discounts,
                    online shopping cashback, and a lifestyle I definitely couldn't afford — I said yes immediately.
                    Who wouldn't?
                  </p>
                </div>
              </motion.div>

              {/* Chapter 2 */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-yellow-100 dark:bg-yellow-900 items-center justify-center z-10">
                  <AlertTriangle className="w-7 h-7 text-yellow-600 dark:text-yellow-400" />
                </div>
                <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                  <span className="text-xs font-bold text-yellow-600 dark:text-yellow-400 uppercase tracking-wider">2013–2014 — The Rookie Mistakes</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">Missed payments, unread statements, and a lot of confusion</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    I used the card — but rarely, and never smartly. Reward categories? Never heard of them.
                    Billing cycles? No idea. I'd get the monthly statement, stare at it like it was written in ancient Sanskrit,
                    and just... move on. And yes, I missed a few payments. Nothing catastrophic, but enough to sting.
                    I was new to money. Genuinely, embarrassingly new.
                  </p>
                </div>
              </motion.div>

              {/* Chapter 3 — The Big Mistake */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-red-100 dark:bg-red-900 items-center justify-center z-10">
                  <Bike className="w-7 h-7 text-red-600 dark:text-red-400" />
                </div>
                <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 border-l-4 border-l-red-400 dark:border-l-red-600">
                  <span className="text-xs font-bold text-red-600 dark:text-red-400 uppercase tracking-wider">2014 — The Big One. Brace Yourself.</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">A Pulsar 150, a smooth-talking showroom guy, and interest-based EMIs</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    I bought my dream bike — a <span className="font-semibold text-gray-800 dark:text-gray-200">Bajaj Pulsar 150</span> — using my credit card.
                    Exciting? Absolutely. Smart? Not even close. The showroom salesperson was kind enough to "help" me convert it into EMIs.
                    What I didn't know — and what nobody bothered to explain — was the difference between
                    <span className="font-semibold text-gray-800 dark:text-gray-200"> no-cost EMI</span> and
                    <span className="font-semibold text-red-600 dark:text-red-400"> interest-bearing EMI</span>.
                    Spoiler: mine was the second kind. I ended up paying significantly more than the bike's actual price,
                    month after month, wondering why my balance wasn't going down as fast as I expected.
                  </p>
                </div>
              </motion.div>

              {/* Chapter 4 — The Minimum Balance Trap */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-orange-100 dark:bg-orange-900 items-center justify-center z-10">
                  <TrendingUp className="w-7 h-7 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                  <span className="text-xs font-bold text-orange-600 dark:text-orange-400 uppercase tracking-wider">The Bonus Mistake</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">Paying the minimum due — thinking I was a genius</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    Here's the thing about 22-year-old me — he thought he was outsmarting the system.
                    "Why pay the full bill when I can just pay the minimum amount due and keep the rest of my salary?"
                    Brilliant, right? <span className="italic">Wrong.</span> The interest was silently compounding at 36–42% per annum on the remaining balance.
                    I was essentially paying the bank to lend me my own money. It took me embarrassingly long to figure this out.
                  </p>
                </div>
              </motion.div>

              {/* Chapter 5 — The Turn */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-green-100 dark:bg-green-900 items-center justify-center z-10">
                  <Lightbulb className="w-7 h-7 text-green-600 dark:text-green-400" />
                </div>
                <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                  <span className="text-xs font-bold text-green-600 dark:text-green-400 uppercase tracking-wider">The Long Way Around</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">From zero financial literacy to obsessive card optimization</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    Over the years, the mistakes got expensive enough that I started paying attention. I read. I researched.
                    I learned what reward categories, billing cycles, milestone benefits, and lounge access actually meant.
                    I went from missing payments to squeezing every rupee of value out of every swipe.
                    Today, I manage multiple cards — each one used for the exact category it rewards best.
                    It took years of trial, error, and a Pulsar 150's worth of tuition fees to get here.
                  </p>
                </div>
              </motion.div>

              {/* Chapter 6 — Why UNGI */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 }}
                className="relative flex gap-6 md:gap-10"
                {...({} as any)}
              >
                <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900 items-center justify-center z-10">
                  <Heart className="w-7 h-7 text-primary-600 dark:text-primary-400" />
                </div>
                <div className="flex-1 bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/30 dark:to-gray-800 rounded-2xl p-6 shadow-sm border border-primary-200 dark:border-primary-800">
                  <span className="text-xs font-bold text-primary-600 dark:text-primary-400 uppercase tracking-wider">And That's Why This Exists</span>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1 mb-2">Nobody should pay Pulsar-level tuition fees to understand credit cards</h3>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    I built <span className="font-semibold text-primary-600 dark:text-primary-400">UNGI SmartCards AI</span> because the journey from clueless to optimized shouldn't take years,
                    missed payments, and interest-laden EMIs. It should take minutes.
                    Whether you just got your first card or you're juggling five of them —
                    this platform helps you know exactly which card to use, when, and why.
                    No jargon. No confusion. Just smart decisions.
                  </p>
                  <p className="text-gray-500 dark:text-gray-400 mt-3 text-sm italic">
                    If this resonates with you, I'd genuinely love your feedback — it helps make this better for everyone.
                  </p>
                </div>
              </motion.div>

            </div>
          </div>

          {/* Feedback CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
            className="text-center mt-16"
            {...({} as any)}
          >
            <p className="text-gray-500 dark:text-gray-400 mb-4">Did this story remind you of your own credit card journey?</p>
            <Link
              to="/register"
              className="inline-flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              <span>Try It — It's Free</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
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
              Ready to Optimize Every Swipe?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join users who are already maximizing their credit card rewards with UNGI SmartCards AI.
            </p>
            <Link
              to="/register"
              className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-4 rounded-lg text-lg font-semibold transition-colors inline-flex items-center space-x-2"
            >
              <span>Get Started Free</span>
              <ArrowRight className="h-5 w-5" />
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
              <Link
                to="/privacy-policy"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                Privacy Policy
              </Link>
              <Link
                to="/terms-of-service"
                className="text-gray-400 hover:text-white transition-colors text-sm"
              >
                Terms of Service
              </Link>
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

export default HomePage; 