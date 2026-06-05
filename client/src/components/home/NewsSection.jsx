import { motion } from 'framer-motion';
import { Link } from 'react-router';

const NewsSection = () => {
  const news = [
    {
      imgUrl:
        'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80',
      category: 'Marché',
      title: "La Côte d'Ivoire consolide sa position mondiale",
      description: 'Analyse des opportunités record dans la filière cajou cette année.',
      date: '12 Juin 2025',
      featured: true,
    },
    {
      imgUrl:
        'https://images.unsplash.com/photo-1595665593673-bf1ad72905c0?auto=format&fit=crop&w=800&q=80',
      category: 'Certification',
      title: 'Nouvelles normes GlobalGap 2025',
      description: 'Coreline Alliance vous accompagne dans la mise en conformité réglementaire.',
      date: '4 Juin 2025',
      featured: false,
    },
    {
      imgUrl:
        'https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=800&q=80',
      category: 'Événement',
      title: 'Coreline au SIA de Paris',
      description: "Retrouvez nos experts au Salon International de l'Agriculture.",
      date: '28 Mai 2025',
      featured: false,
    },
  ];

  return (
    <section className="section section-alt" id="actualites">
      <div className="container">
        <div className="section-header">
          <span className="badge">Actualités</span>
          <h2>Dernières Analyses & Insights</h2>
          <p>Suivez l'évolution de nos projets et nos décryptages stratégiques.</p>
        </div>

        <div className="news-grid">
          {news.map((item, i) => (
            <motion.div
              className={`news-card ${item.featured ? 'featured-news' : ''}`}
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <div
                className="news-img-container"
                style={{ height: item.featured ? '240px' : '160px', overflow: 'hidden' }}
              >
                <img
                  src={item.imgUrl}
                  alt={item.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>
              <div className="news-content">
                <span className="news-category">{item.category}</span>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <div className="news-meta">
                  <span className="news-date">{item.date}</span>
                  <Link
                    to={`/actualites/iywf-2026`}
                    className="news-link"
                    aria-label={`Lire la suite de l'article : ${item.title}`}
                  >
                    Lire la suite
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default NewsSection;
