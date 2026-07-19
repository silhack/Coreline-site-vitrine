import { motion } from 'framer-motion';
import { Globe, Lightbulb, ShieldCheck, Target, Users } from 'lucide-react';
import { useEffect } from 'react';
import SEO from '../components/common/SEO';
import CeoWord from '../components/home/CeoWord';
import TeamSection from '../components/home/TeamSection';

const AboutPage = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <main className="about-page" style={{ paddingTop: '100px' }}>
      <SEO
        title="À Propos"
        description="Découvrez Coreline Alliance, un catalyseur de projets durables en Afrique, mobilisant expertises et financements institutionnels."
      />
      {/* 1. Hero / Executive Summary */}
      <section className="section">
        <div className="container">
          <div className="grid-2">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <span className="badge" style={{ marginBottom: '1.5rem', display: 'inline-block' }}>
                Executive Summary
              </span>
              <h1
                style={{
                  fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
                  fontWeight: '900',
                  color: 'var(--secondary)',
                  marginBottom: '1.5rem',
                  lineHeight: '1.1',
                }}
              >
                Catalyseur de <span style={{ color: 'var(--primary)' }}>Projets Durables</span>
              </h1>
              <p
                style={{
                  fontSize: '1.1rem',
                  color: 'var(--gray-600)',
                  lineHeight: '1.8',
                  marginBottom: '2rem',
                }}
              >
                Coreline est une alliance internationale d'experts en finance, agro-industrie,
                énergie et technologies œuvrant main dans la main pour accélérer le développement de
                projets durables au service des communautés locales africaines.
              </p>
              <div style={{ display: 'flex', gap: '2rem' }}>
                <div>
                  <h4 style={{ fontSize: 'clamp(1.5rem, 5vw, 2rem)', color: 'var(--primary)', margin: 0 }}>3</h4>
                  <p
                    style={{
                      color: 'var(--gray-500)',
                      fontSize: '0.9rem',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                    }}
                  >
                    Transitions (Alim., Énerg., Clim.)
                  </p>
                </div>
                <div>
                  <h4 style={{ fontSize: 'clamp(1.5rem, 5vw, 2rem)', color: 'var(--primary)', margin: 0 }}>2026</h4>
                  <p
                    style={{
                      color: 'var(--gray-500)',
                      fontSize: '0.9rem',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                    }}
                  >
                    Objectif IYWF
                  </p>
                </div>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <img
                src="https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=800&q=80"
                alt="Coreline Team Meeting"
                style={{
                  width: '100%',
                  borderRadius: 'var(--radius-lg)',
                  boxShadow: 'var(--shadow-premium)',
                }}
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* 2. Notre point de départ */}
      <section className="section section-alt">
        <div className="container">
          <div className="grid-2">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h3
                style={{
                  fontSize: 'clamp(1.5rem, 4vw, 2rem)',
                  fontWeight: '800',
                  marginBottom: '1.5rem',
                  color: 'var(--secondary)',
                }}
              >
                Notre Point de Départ
              </h3>
              <ul
                style={{
                  listStyle: 'none',
                  padding: 0,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '1.5rem',
                }}
              >
                <li style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  <Users className="text-primary" style={{ flexShrink: 0, marginTop: '4px' }} />
                  <span style={{ fontSize: '1.1rem', color: 'var(--gray-700)' }}>
                    L'Afrique comptera <strong>2,5 milliards d'habitants d'ici 2050</strong>, avec
                    une demande alimentaire et énergétique en forte croissance.
                  </span>
                </li>
                <li style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  <Globe className="text-primary" style={{ flexShrink: 0, marginTop: '4px' }} />
                  <span style={{ fontSize: '1.1rem', color: 'var(--gray-700)' }}>
                    Le continent importe encore plus de <strong>50 milliards USD</strong> de
                    produits alimentaires par an et près de <strong>600 M d'Africains</strong>{' '}
                    vivent sans accès à l'électricité.
                  </span>
                </li>
                <li style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  <Target className="text-primary" style={{ flexShrink: 0, marginTop: '4px' }} />
                  <span style={{ fontSize: '1.1rem', color: 'var(--gray-700)' }}>
                    Les besoins d'investissements climatiques sont estimés à 2 800 milliards USD
                    d'ici 2030, mais seuls <strong>5 %</strong> atteignent le continent.
                  </span>
                </li>
              </ul>
            </motion.div>

            <motion.div
              style={{
                background: 'var(--white)',
                padding: '3rem',
                borderRadius: 'var(--radius-lg)',
                boxShadow: 'var(--shadow-premium)',
              }}
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h4
                style={{
                  fontSize: '1.5rem',
                  fontWeight: '800',
                  marginBottom: '1.5rem',
                  color: 'var(--secondary)',
                }}
              >
                Notre Vision & Mission
              </h4>
              <p style={{ color: 'var(--gray-600)', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                Coreline mobilise les expertises, les financements et l'innovation technologique au
                service d'une industrialisation durable qui crée de la valeur pour les communautés
                locales, tout en contribuant à la transition climatique et à la préservation de la
                biodiversité.
              </p>
              <div
                style={{
                  padding: '1.5rem',
                  background: 'rgba(212, 175, 55, 0.1)',
                  borderRadius: '12px',
                  borderLeft: '4px solid var(--primary)',
                }}
              >
                <strong
                  style={{ color: 'var(--primary)', display: 'block', marginBottom: '0.5rem' }}
                >
                  Notre Mission :
                </strong>
                <span style={{ fontSize: '0.95rem' }}>
                  Mettre à contribution nos expertises pour identifier, structurer des projets
                  durables et viables, et mobiliser les financements pour accélérer leur
                  développement.
                </span>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 3. Nos Piliers d'Action (Corelines) */}
      <section className="section">
        <div className="container">
          <div
            className="section-header"
            style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto 4rem auto' }}
          >
            <h2>Nos Piliers d'Action (Corelines)</h2>
            <p className="lead">
              Une assistance adaptée aux réalités locales, répondant aux meilleurs standards
              internationaux.
            </p>
          </div>

          <div className="corelines-grid">
            <motion.div
              style={{
                padding: '2.5rem',
                backgroundColor: 'var(--white)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--gray-100)',
                boxShadow: 'var(--shadow)',
              }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
            >
              <h3
                style={{
                  fontSize: '1.5rem',
                  color: 'var(--secondary)',
                  marginBottom: '1rem',
                  borderBottom: '2px solid var(--primary)',
                  paddingBottom: '0.5rem',
                  display: 'inline-block',
                }}
              >
                Coreline Origine
              </h3>
              <p
                style={{
                  color: 'var(--gray-600)',
                  lineHeight: '1.6',
                  fontWeight: '500',
                  marginBottom: '1rem',
                }}
              >
                Identifier, structurer et développer un pipeline de projets viables.
              </p>
              <ul
                style={{
                  color: 'var(--gray-600)',
                  fontSize: '0.95rem',
                  paddingLeft: '1.2rem',
                  lineHeight: '1.5',
                }}
              >
                <li style={{ marginBottom: '0.5rem' }}>
                  Programme de structuration (Agroénergie & Landscape)
                </li>
                <li>
                  Préparation à l'investissement (Maturité, Structuration ESG/Tech/Fin, Investment
                  memo)
                </li>
              </ul>
            </motion.div>

            <motion.div
              style={{
                padding: '2.5rem',
                backgroundColor: 'var(--white)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--gray-100)',
                boxShadow: 'var(--shadow)',
              }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <h3
                style={{
                  fontSize: '1.5rem',
                  color: 'var(--secondary)',
                  marginBottom: '1rem',
                  borderBottom: '2px solid var(--primary)',
                  paddingBottom: '0.5rem',
                  display: 'inline-block',
                }}
              >
                Coreline Invest
              </h3>
              <p
                style={{
                  color: 'var(--gray-600)',
                  lineHeight: '1.6',
                  fontWeight: '500',
                  marginBottom: '1rem',
                }}
              >
                Codévelopper des solutions de financement et gérer le portefeuille.
              </p>
              <ul
                style={{
                  color: 'var(--gray-600)',
                  fontSize: '0.95rem',
                  paddingLeft: '1.2rem',
                  lineHeight: '1.5',
                }}
              >
                <li style={{ marginBottom: '0.5rem' }}>
                  Mobilisation des capitaux locaux et internationaux
                </li>
                <li>
                  Gestion de portefeuille (Suivi financier, empreinte ESG, accompagnement
                  international)
                </li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 4. Core Values (from core.txt) */}
      <section className="section section-alt">
        <div className="container">
          <div
            className="section-header"
            style={{ textAlign: 'center', margin: '0 auto 4rem auto' }}
          >
            <h2>Nos Valeurs Coreline</h2>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '2rem',
            }}
          >
            {[
              {
                icon: ShieldCheck,
                title: 'Respect',
                desc: "Agir dans le respect des personnes, des communautés et des écosystèmes, en plaçant l'éthique et la responsabilité au cœur des actions.",
              },
              {
                icon: Lightbulb,
                title: 'Innovation & Excellence',
                desc: "Encourager la créativité et les solutions innovantes tout en recherchant l'excellence, pour bâtir des initiatives durables.",
              },
              {
                icon: Users,
                title: 'Solidarité',
                desc: "Promouvoir l'entraide, la coopération, le partage des connaissances et de la valeur pour soutenir la création de valeur durable.",
              },
            ].map((v, i) => {
              const Icon = v.icon;
              return (
                <motion.div
                  key={i}
                  style={{
                    textAlign: 'center',
                    padding: '2.5rem',
                    backgroundColor: 'var(--white)',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--gray-100)',
                    boxShadow: 'var(--shadow)',
                  }}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                >
                  <div
                    style={{
                      display: 'inline-flex',
                      padding: '15px',
                      backgroundColor: 'rgba(212, 175, 55, 0.1)',
                      borderRadius: '50%',
                      marginBottom: '1.5rem',
                    }}
                  >
                    <Icon size={32} color="var(--primary)" />
                  </div>
                  <h4
                    style={{
                      fontSize: '1.3rem',
                      color: 'var(--secondary)',
                      marginBottom: '1rem',
                      fontWeight: '800',
                    }}
                  >
                    {v.title}
                  </h4>
                  <p style={{ color: 'var(--gray-600)', fontSize: '1rem', lineHeight: '1.6' }}>
                    {v.desc}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 5. Le Mot du Président */}
      <CeoWord />

      {/* 6. La Gouvernance (Partenaires et Équipe) */}
      <TeamSection />
    </main>
  );
};

export default AboutPage;
