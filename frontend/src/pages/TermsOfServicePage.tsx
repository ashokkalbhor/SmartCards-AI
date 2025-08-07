import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, FileText, AlertTriangle, CheckCircle, Shield, Users, CreditCard, Scale } from 'lucide-react';

const TermsOfServicePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link
                to="/"
                className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Back to Home</span>
              </Link>
            </div>
            <div className="flex items-center space-x-2">
              <FileText className="w-6 h-6 text-primary-600 dark:text-primary-400" />
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Terms of Service</h1>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Terms of Service
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Last updated: January 2025
            </p>
          </div>

          <div className="space-y-8">
            {/* Introduction */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <FileText className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Introduction
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                These Terms of Service ("Terms") govern your use of UNGI SmartCards AI ("Service"), operated by UNGI SmartCards AI ("we," "us," or "our"). By accessing or using our Service, you agree to be bound by these Terms.
              </p>
              <p className="text-gray-600 dark:text-gray-300">
                Our Service provides credit card recommendations, comparisons, and community features to help users make informed financial decisions.
              </p>
            </section>

            {/* Acceptance of Terms */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <CheckCircle className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Acceptance of Terms
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                By using our Service, you acknowledge that you have read, understood, and agree to be bound by these Terms. If you do not agree to these Terms, you must not use our Service.
              </p>
              <p className="text-gray-600 dark:text-gray-300">
                We reserve the right to modify these Terms at any time. Changes will be effective immediately upon posting. Your continued use of the Service after changes constitutes acceptance of the new Terms.
              </p>
            </section>

            {/* Service Description */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <CreditCard className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Service Description
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                UNGI SmartCards AI provides the following services:
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 ml-4">
                <li><strong>Credit Card Recommendations:</strong> AI-powered suggestions based on your preferences and spending patterns</li>
                <li><strong>Card Comparisons:</strong> Side-by-side comparison of credit card features, rewards, and fees</li>
                <li><strong>Community Features:</strong> User reviews, discussions, and shared experiences</li>
                <li><strong>Financial Tools:</strong> Calculators and analysis tools for credit card benefits</li>
                <li><strong>Educational Content:</strong> Articles and guides about credit cards and financial management</li>
              </ul>
            </section>

            {/* User Accounts */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Users className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                User Accounts
              </h2>
              <div className="space-y-4">
                <p className="text-gray-600 dark:text-gray-300">
                  To access certain features of our Service, you may need to create an account. You agree to:
                </p>
                <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 ml-4">
                  <li>Provide accurate, current, and complete information during registration</li>
                  <li>Maintain and update your account information to keep it accurate and current</li>
                  <li>Protect your account credentials and not share them with others</li>
                  <li>Accept responsibility for all activities under your account</li>
                  <li>Notify us immediately of any unauthorized use of your account</li>
                </ul>
                <p className="text-gray-600 dark:text-gray-300">
                  We reserve the right to terminate accounts that violate these Terms or engage in fraudulent activity.
                </p>
              </div>
            </section>

            {/* Acceptable Use */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Shield className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Acceptable Use
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                You agree to use our Service only for lawful purposes and in accordance with these Terms. You agree not to:
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 ml-4">
                <li>Use the Service for any illegal or unauthorized purpose</li>
                <li>Violate any applicable laws or regulations</li>
                <li>Infringe on the rights of others, including intellectual property rights</li>
                <li>Submit false, misleading, or fraudulent information</li>
                <li>Attempt to gain unauthorized access to our systems or other users' accounts</li>
                <li>Use automated systems to access the Service without our permission</li>
                <li>Interfere with or disrupt the Service or servers</li>
                <li>Post content that is harmful, offensive, or inappropriate</li>
                <li>Use the Service to promote competing services without our consent</li>
              </ul>
            </section>

            {/* Content and Intellectual Property */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Scale className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Content and Intellectual Property
              </h2>
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Our Content</h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    The Service and its original content, features, and functionality are owned by UNGI SmartCards AI and are protected by international copyright, trademark, and other intellectual property laws.
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">User Content</h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    You retain ownership of content you submit to our Service. By submitting content, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, modify, and distribute your content in connection with our Service.
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Third-Party Content</h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    Our Service may contain links to third-party websites and content. We are not responsible for the content or practices of third-party sites.
                  </p>
                </div>
              </div>
            </section>

            {/* Disclaimers */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <AlertTriangle className="w-6 h-6 mr-2 text-primary-600 dark:text-primary-400" />
                Disclaimers
              </h2>
              <div className="space-y-4">
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Financial Advice Disclaimer:</strong> Our Service provides information and recommendations for educational purposes only. We are not a financial advisor, and our recommendations should not be considered as financial advice. Always consult with qualified financial professionals before making financial decisions.
                </p>
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Accuracy of Information:</strong> While we strive to provide accurate and up-to-date information, we cannot guarantee the accuracy, completeness, or timeliness of any information on our Service. Credit card terms and offers may change without notice.
                </p>
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Service Availability:</strong> We do not guarantee that our Service will be available at all times or that it will be error-free. We may modify, suspend, or discontinue the Service at any time.
                </p>
              </div>
            </section>

            {/* Limitation of Liability */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Limitation of Liability
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                To the maximum extent permitted by law, UNGI SmartCards AI shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to:
              </p>
              <ul className="list-disc list-inside text-gray-600 dark:text-gray-300 space-y-2 ml-4">
                <li>Loss of profits, data, or business opportunities</li>
                <li>Damages resulting from financial decisions made based on our recommendations</li>
                <li>Damages caused by third-party services or content</li>
                <li>Damages resulting from unauthorized access to your account</li>
                <li>Any other damages arising from your use of the Service</li>
              </ul>
            </section>

            {/* Privacy and Data */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Privacy and Data Protection
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                Your privacy is important to us. Our collection and use of personal information is governed by our Privacy Policy, which is incorporated into these Terms by reference. By using our Service, you consent to our collection and use of information as described in our Privacy Policy.
              </p>
            </section>

            {/* Termination */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Termination
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                We may terminate or suspend your account and access to our Service immediately, without prior notice, for any reason, including if you breach these Terms.
              </p>
              <p className="text-gray-600 dark:text-gray-300">
                Upon termination, your right to use the Service will cease immediately. We may delete your account and data, though some information may be retained as required by law or for legitimate business purposes.
              </p>
            </section>

            {/* Governing Law */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Governing Law
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which UNGI SmartCards AI operates, without regard to its conflict of law provisions. Any disputes arising from these Terms or your use of the Service shall be resolved in the courts of that jurisdiction.
              </p>
            </section>

            {/* Severability */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Severability
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                If any provision of these Terms is found to be unenforceable or invalid, that provision will be limited or eliminated to the minimum extent necessary so that these Terms will otherwise remain in full force and effect.
              </p>
            </section>

            {/* Contact Information */}
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Contact Us
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Email:</strong> legal@ungismartcards.ai
                </p>
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Address:</strong> UNGI SmartCards AI, Legal Team
                </p>
                <p className="text-gray-600 dark:text-gray-300">
                  <strong>Response Time:</strong> We aim to respond to legal inquiries within 5 business days
                </p>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TermsOfServicePage; 