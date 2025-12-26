import React from 'react';
import { Link } from 'react-router-dom';
import { Phone, Mail, MapPin, Facebook, Instagram, Twitter, Youtube } from 'lucide-react';
import { useData } from '../../context/DataContext';

const Footer = () => {
  const { categories, siteSettings } = useData();

  const LOGO_URL = siteSettings.logo || "https://customer-assets.emergentagent.com/job_70b8c44d-b0eb-46ab-b798-c90870274405/artifacts/5olvlaa7_WhatsApp%20Image%202025-12-26%20at%2013.46.33.jpeg";
  const callLink = `tel:+91${siteSettings.phone}`;

  // Social media links from settings
  const socialLinks = [
    { icon: Facebook, link: siteSettings.facebookLink, label: 'Facebook' },
    { icon: Instagram, link: siteSettings.instagramLink, label: 'Instagram' },
    { icon: Twitter, link: siteSettings.twitterLink, label: 'Twitter' },
    { icon: Youtube, link: siteSettings.youtubeLink, label: 'YouTube' }
  ].filter(social => social.link); // Only show links that are configured

  return (
    <footer className="bg-[#2d1810] text-white" id="contact">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Info */}
          <div>
            <Link to="/" className="flex items-center gap-3 mb-4">
              <img 
                src={LOGO_URL} 
                alt={siteSettings.businessName} 
                className="h-16 w-16 rounded-full object-cover border-2 border-amber-400"
              />
              <div>
                <h2 className="text-xl font-bold">{siteSettings.businessName}</h2>
                <p className="text-amber-300 italic text-sm">{siteSettings.slogan}</p>
              </div>
            </Link>
            <p className="text-gray-300 text-sm leading-relaxed mb-4">
              Premium quality dry fruits, nuts, and seeds delivered to your doorstep. 
              We ensure freshness and quality in every pack.
            </p>
            {socialLinks.length > 0 && (
              <div className="flex gap-3">
                {socialLinks.map((social, index) => (
                  <a 
                    key={index}
                    href={social.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="w-10 h-10 bg-amber-700 hover:bg-amber-600 rounded-full flex items-center justify-center transition-colors"
                    aria-label={social.label}
                  >
                    <social.icon className="w-5 h-5" />
                  </a>
                ))}
              </div>
            )}
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-amber-300">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">Home</Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">All Products</Link>
              </li>
              <li>
                <a href="#about" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">About Us</a>
              </li>
              <li>
                <a href="#contact" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">Contact Us</a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">Privacy Policy</a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-amber-300 transition-colors text-sm">Terms & Conditions</a>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-amber-300">Categories</h3>
            <ul className="space-y-2">
              {categories.map((cat) => (
                <li key={cat.id}>
                  <Link 
                    to={`/products?category=${cat.slug}`} 
                    className="text-gray-300 hover:text-amber-300 transition-colors text-sm"
                  >
                    {cat.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-amber-300">Contact Us</h3>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <Phone className="w-5 h-5 text-amber-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-400">Call us</p>
                  <a href={callLink} className="text-white hover:text-amber-300 transition-colors">
                    +91 {siteSettings.phone}
                  </a>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-amber-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-400">Email us</p>
                  <a href={`mailto:${siteSettings.email}`} className="text-white hover:text-amber-300 transition-colors">
                    {siteSettings.email}
                  </a>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-amber-400 mt-0.5" />
                <div>
                  <p className="text-sm text-gray-400">Visit us</p>
                  <p className="text-white text-sm">{siteSettings.address}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-amber-900">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              © 2025 {siteSettings.businessName}. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <img src="https://img.icons8.com/color/48/visa.png" alt="Visa" className="h-8" />
              <img src="https://img.icons8.com/color/48/mastercard.png" alt="Mastercard" className="h-8" />
              <img src="https://img.icons8.com/color/48/paypal.png" alt="PayPal" className="h-8" />
              <img src="https://img.icons8.com/color/48/google-pay-india.png" alt="GPay" className="h-8" />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
