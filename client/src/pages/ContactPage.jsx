import { motion } from 'framer-motion';
import { Building, Mail, Phone } from 'lucide-react';
import { useEffect, useId, useState } from 'react';
import SEO from '../components/common/SEO';

const faqData = [
  {
    q: 'Comment devenir partenaire de Coreline Alliance ?',
    a: 'Nous sommes toujours à la recherche d\'expertises complémentaires. Veuillez utiliser le formulaire de contact en précisant "Partenariat" dans l\'objet du message.',
  },
  {
    q: 'Dans quels pays opérez-vous spécifiquement ?',
    a: "Bien que notre réseau soit international, nos opérations de terrain se concentrent principalement en Afrique de l'Ouest et Centrale (Sénégal, Côte d'Ivoire, Cameroun).",
  },
  {
    q: 'Où se trouve le siège social ?',
    a: "Notre siège de coordination est situé à Paris, France, avec des bureaux régionaux pour assurer un ancrage direct sur nos zones d'intervention.",
  },
];

const ContactPage = () => {
  const [openFaq, setOpenFaq] = useState(0);
  const [formStatus, setFormStatus] = useState({ type: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const formId = useId();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleSubmit = async e => {
    e.preventDefault();
    setIsSubmitting(true);
    setFormStatus({ type: '', message: '' });

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // 1. Honeypot check (Anti-spam)
    if (data.website) {
      console.warn('Spam detected');
      setIsSubmitting(false);
      return;
    }

    // 2. Basic Validation
    if (!data.firstname || !data.lastname || !data.email || !data.message) {
      setFormStatus({ type: 'error', message: 'Veuillez remplir tous les champs obligatoires.' });
      setIsSubmitting(false);
      return;
    }

    // 3. Email Validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
      setFormStatus({ type: 'error', message: 'Veuillez entrer une adresse email valide.' });
      setIsSubmitting(false);
      return;
    }

    // Utilise notre API de messagerie souveraine
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const CONTACT_API_URL = `${API_URL}/api/contact`;

    // Restructuration des données pour correspondre au schéma attendu par l'API
    const payload = {
      name: `${data.firstname} ${data.lastname}`,
      email: data.email,
      subject: data.subject,
      message: data.message
    };

    try {
      const response = await fetch(CONTACT_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        setFormStatus({
          type: 'success',
          message: 'Votre message a été envoyé avec succès ! Notre équipe vous répondra sous 48h.',
        });
        e.target.reset();

        // Le message disparaît après 5 secondes
        setTimeout(() => setFormStatus({ type: '', message: '' }), 5000);
      } else {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || "Erreur lors de l'envoi");
      }
    } catch (error) {
      setFormStatus({
        type: 'error',
        message:
          error.message || "Une erreur est survenue lors de l'envoi. Veuillez réessayer ou nous contacter directement par email.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="contact-page" style={{ paddingTop: '100px' }}>
      <SEO
        title="Contact"
        description="Contactez Coreline Alliance pour vos projets d'investissement durable en Afrique. Notre équipe d'experts vous accompagne dans la structuration et le financement."
      />
      <section className="section">
        <div className="container">
          <div className="section-header" style={{ textAlign: 'center', marginBottom: '4rem' }}>
            <span className="badge">On vous écoute</span>
            <h2>Contactez l'Alliance</h2>
            <p className="lead" style={{ marginTop: '1rem' }}>
              Une question, un projet, une opportunité ? Notre équipe d'experts est prête à
              échanger.
            </p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'minmax(0,1fr) minmax(0,1fr)',
              gap: '4rem',
            }}
          >
            {/* Form Column */}
            <motion.div
              style={{
                backgroundColor: 'var(--white)',
                padding: '3rem',
                borderRadius: 'var(--radius-lg)',
                boxShadow: 'var(--shadow-premium)',
                border: '1px solid var(--gray-100)',
              }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h3 style={{ fontSize: '1.5rem', color: 'var(--secondary)', marginBottom: '2rem' }}>
                Envoyez-nous un message
              </h3>

              {formStatus.message && (
                <div
                  style={{
                    padding: '1rem',
                    borderRadius: '8px',
                    marginBottom: '1.5rem',
                    backgroundColor: formStatus.type === 'success' ? '#dcfce7' : '#fee2e2',
                    color: formStatus.type === 'success' ? '#166534' : '#991b1b',
                    fontSize: '0.9rem',
                    fontWeight: '600',
                  }}
                >
                  {formStatus.message}
                </div>
              )}

              <form
                onSubmit={handleSubmit}
                style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
              >
                {/* Honeypot field - hidden from users */}
                <input
                  type="text"
                  name="website"
                  style={{ display: 'none' }}
                  tabIndex="-1"
                  autoComplete="off"
                />

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                  <div className="form-group">
                    <label
                      htmlFor={`${formId}-firstname`}
                      style={{
                        display: 'block',
                        fontSize: '0.9rem',
                        fontWeight: 'bold',
                        color: 'var(--secondary)',
                        marginBottom: '0.5rem',
                      }}
                    >
                      Prénom
                    </label>
                    <input
                      name="firstname"
                      id={`${formId}-firstname`}
                      type="text"
                      className="form-control"
                      placeholder="Jean"
                      required
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: '1px solid var(--gray-200)',
                        borderRadius: '8px',
                      }}
                    />
                  </div>
                  <div className="form-group">
                    <label
                      htmlFor={`${formId}-lastname`}
                      style={{
                        display: 'block',
                        fontSize: '0.9rem',
                        fontWeight: 'bold',
                        color: 'var(--secondary)',
                        marginBottom: '0.5rem',
                      }}
                    >
                      Nom
                    </label>
                    <input
                      name="lastname"
                      id={`${formId}-lastname`}
                      type="text"
                      className="form-control"
                      placeholder="Dupont"
                      required
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: '1px solid var(--gray-200)',
                        borderRadius: '8px',
                      }}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label
                    htmlFor={`${formId}-email`}
                    style={{
                      display: 'block',
                      fontSize: '0.9rem',
                      fontWeight: 'bold',
                      color: 'var(--secondary)',
                      marginBottom: '0.5rem',
                    }}
                  >
                    Email Professionnel
                  </label>
                  <input
                    name="email"
                    id={`${formId}-email`}
                    type="email"
                    className="form-control"
                    placeholder="jean.dupont@entreprise.com"
                    required
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '1px solid var(--gray-200)',
                      borderRadius: '8px',
                    }}
                  />
                </div>

                <div className="form-group">
                  <label
                    htmlFor={`${formId}-subject`}
                    style={{
                      display: 'block',
                      fontSize: '0.9rem',
                      fontWeight: 'bold',
                      color: 'var(--secondary)',
                      marginBottom: '0.5rem',
                    }}
                  >
                    Sujet / Motif
                  </label>
                  <select
                    name="subject"
                    id={`${formId}-subject`}
                    className="form-control"
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '1px solid var(--gray-200)',
                      borderRadius: '8px',
                      backgroundColor: 'white',
                    }}
                  >
                    <option value="Information">Demande d'information</option>
                    <option value="Projet">Proposition de projet</option>
                    <option value="Partenariat">Partenariat institutionnel</option>
                    <option value="Presse">Presse / Média</option>
                  </select>
                </div>

                <div className="form-group">
                  <label
                    htmlFor={`${formId}-message`}
                    style={{
                      display: 'block',
                      fontSize: '0.9rem',
                      fontWeight: 'bold',
                      color: 'var(--secondary)',
                      marginBottom: '0.5rem',
                    }}
                  >
                    Message
                  </label>
                  <textarea
                    name="message"
                    id={`${formId}-message`}
                    className="form-control"
                    rows="5"
                    placeholder="Détaillez votre demande ici..."
                    required
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '1px solid var(--gray-200)',
                      borderRadius: '8px',
                      resize: 'vertical',
                    }}
                  ></textarea>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn btn-primary"
                  style={{
                    padding: '15px',
                    fontSize: '1.05rem',
                    fontWeight: 'bold',
                    marginTop: '1rem',
                    opacity: isSubmitting ? 0.7 : 1,
                    cursor: isSubmitting ? 'not-allowed' : 'pointer',
                  }}
                >
                  {isSubmitting ? 'Envoi en cours...' : 'Envoyer le message'}
                </button>
              </form>
            </motion.div>

            {/* Info Column */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <div style={{ marginBottom: '4rem' }}>
                <h3
                  style={{ fontSize: '1.5rem', color: 'var(--secondary)', marginBottom: '1.5rem' }}
                >
                  Informations de contact
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                    <div
                      style={{
                        backgroundColor: 'rgba(212, 175, 55, 0.1)',
                        padding: '12px',
                        borderRadius: '50%',
                        color: 'var(--primary)',
                      }}
                    >
                      <Building size={24} />
                    </div>
                    <div>
                      <h4 style={{ margin: '0 0 0.25rem 0', color: 'var(--secondary)' }}>
                        Siège de l'Alliance
                      </h4>
                      <p style={{ margin: 0, color: 'var(--gray-600)', lineHeight: '1.5' }}>
                        75008 Paris,
                        <br />
                        France
                      </p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                    <div
                      style={{
                        backgroundColor: 'rgba(212, 175, 55, 0.1)',
                        padding: '12px',
                        borderRadius: '50%',
                        color: 'var(--primary)',
                      }}
                    >
                      <Mail size={24} />
                    </div>
                    <div>
                      <h4 style={{ margin: '0 0 0.25rem 0', color: 'var(--secondary)' }}>Email</h4>
                      <p style={{ margin: 0, color: 'var(--gray-600)', lineHeight: '1.5' }}>
                        contact@coreline-partners.com
                        <br />
                        presse@coreline-partners.com
                      </p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                    <div
                      style={{
                        backgroundColor: 'rgba(212, 175, 55, 0.1)',
                        padding: '12px',
                        borderRadius: '50%',
                        color: 'var(--primary)',
                      }}
                    >
                      <Phone size={24} />
                    </div>
                    <div>
                      <h4 style={{ margin: '0 0 0.25rem 0', color: 'var(--secondary)' }}>
                        Téléphone
                      </h4>
                      <p style={{ margin: 0, color: 'var(--gray-600)', lineHeight: '1.5' }}>
                        +33 (0) 1 80 XX XX XX
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* FAQ */}
              <div>
                <h3
                  style={{ fontSize: '1.5rem', color: 'var(--secondary)', marginBottom: '1.5rem' }}
                >
                  Foire Aux Questions
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {faqData.map((item, index) => (
                    <div
                      key={index}
                      style={{
                        border: '1px solid var(--gray-200)',
                        borderRadius: 'var(--radius)',
                        overflow: 'hidden',
                      }}
                    >
                      <button
                        onClick={() => setOpenFaq(openFaq === index ? -1 : index)}
                        aria-expanded={openFaq === index}
                        aria-controls={`faq-answer-${index}`}
                        style={{
                          width: '100%',
                          padding: '1rem',
                          backgroundColor: openFaq === index ? 'var(--gray-50)' : 'white',
                          border: 'none',
                          textAlign: 'left',
                          fontWeight: 'bold',
                          color: 'var(--secondary)',
                          cursor: 'pointer',
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                        }}
                      >
                        {item.q}
                        <span
                          style={{
                            color: 'var(--primary)',
                            transform: openFaq === index ? 'rotate(180deg)' : 'none',
                            transition: 'transform 0.3s',
                          }}
                        >
                          ▼
                        </span>
                      </button>
                      <div
                        id={`faq-answer-${index}`}
                        role="region"
                        aria-labelledby={`faq-question-${index}`}
                        style={{
                          padding: openFaq === index ? '1rem' : '0 1rem',
                          height: openFaq === index ? 'auto' : '0',
                          overflow: 'hidden',
                          color: 'var(--gray-600)',
                          backgroundColor: 'white',
                          borderTop: openFaq === index ? '1px solid var(--gray-100)' : 'none',
                        }}
                      >
                        {item.a}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </main>
  );
};

export default ContactPage;
