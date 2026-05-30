import { motion } from 'framer-motion';
import { MapPin } from 'lucide-react';
import { useState } from 'react';

const ContactSection = () => {
  const [formState, setFormState] = useState({ name: '', email: '', subject: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Honeypot check
    if (data.website) return;

    setIsSubmitting(true);

    // Utilise notre API de messagerie souveraine
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const CONTACT_API_URL = `${API_URL}/api/contact`;

    try {
      const response = await fetch(CONTACT_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        setIsSent(true);
        setFormState({ name: '', email: '', subject: '', message: '' });
        e.target.reset();
        // Le message disparaît après 5 secondes
        setTimeout(() => setIsSent(false), 5000);
      } else {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || "Erreur lors de l'envoi");
      }
    } catch (error) {
      alert(error.message || 'Une erreur est survenue. Veuillez réessayer ou nous contacter directement par email.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="contact-section" id="contact">
      <div className="container contact-layout">
        <motion.div
          className="contact-text"
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <span className="badge badge-light">Contact</span>
          <h2>Parlons de votre prochain projet d'impact</h2>
          <p>
            Nos experts sont à votre disposition pour étudier vos opportunités d'investissement et
            de structuration.
          </p>

          <div className="contact-info">
            <div className="contact-info-item">
              <div className="info-icon-box">
                <MapPin />
              </div>
              <div className="info-text">
                <strong>Siège Paris</strong>
                <span>45b Boulevard Jourdan, Paris, 75014</span>
                <span style={{ fontSize: '0.85rem', opacity: 0.8 }}>Tél: + (33) 7 53 34 25 98</span>
              </div>
            </div>

            <div className="contact-info-item">
              <div className="info-icon-box">
                <MapPin />
              </div>
              <div className="info-text">
                <strong>Bureau Abidjan</strong>
                <span>Cocody, Angré 7ème Tranche</span>
                <span style={{ fontSize: '0.85rem', opacity: 0.8 }}>
                  Tél: + (225) 07 58 42 26 65
                </span>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.form
          className="contact-form"
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          onSubmit={handleSubmit}
        >
          {/* Honeypot field */}
          <input
            type="text"
            name="website"
            style={{ display: 'none' }}
            tabIndex="-1"
            autoComplete="off"
          />

          {isSent && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              style={{
                gridColumn: '1 / -1',
                padding: '1rem',
                borderRadius: '8px',
                marginBottom: '1rem',
                backgroundColor: '#fef9c3',
                color: '#854d0e',
                fontSize: '0.9rem',
                fontWeight: '600',
                textAlign: 'center',
                border: '1px solid #fef08a',
              }}
            >
              Message envoyé ! Nous vous répondrons sous 24h.
            </motion.div>
          )}

          <div className="form-group">
            <label htmlFor="name">Nom complet</label>
            <input
              type="text"
              id="name"
              name="name"
              placeholder="Jean Dupont"
              required
              value={formState.name}
              onChange={e => setFormState({ ...formState, name: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email professionnel</label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="jean@entreprise.com"
              required
              value={formState.email}
              onChange={e => setFormState({ ...formState, email: e.target.value })}
            />
          </div>
          <div className="form-group full-width">
            <label htmlFor="subject">Je souhaite échanger sur :</label>
            <select
              id="subject"
              name="subject"
              required
              value={formState.subject}
              onChange={e => setFormState({ ...formState, subject: e.target.value })}
            >
              <option value="">Sélectionner une thématique</option>
              <option>Structuration de projet (Coreline Origine)</option>
              <option>Investissement & Capital (Coreline Invest)</option>
              <option>Partenariat IYWF 2026</option>
              <option>Expertise Conseil & Strategy</option>
              <option>Autre demande</option>
            </select>
          </div>
          <div className="form-group full-width">
            <label htmlFor="message">Message</label>
            <textarea
              id="message"
              name="message"
              rows="5"
              placeholder="Détaillez votre demande ici..."
              required
              value={formState.message}
              onChange={e => setFormState({ ...formState, message: e.target.value })}
            ></textarea>
          </div>

          <button type="submit" className="btn-contact" disabled={isSubmitting}>
            {isSubmitting ? 'Envoi en cours...' : 'Envoyer le message'}
          </button>
        </motion.form>
      </div>
    </section>
  );
};

export default ContactSection;
