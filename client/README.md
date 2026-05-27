# Coreline Alliance — Site Vitrine (Frontend)

Application **React** du site vitrine de **Coreline Alliance**, une alliance internationale d'experts spécialisée dans l'investissement durable en Afrique. Le site présente les services, les solutions, l'équipe et propose un formulaire de contact connecté au backend FastAPI.

---

## Table des Matières

- [Aperçu](#aperçu)
- [Stack Technique](#stack-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Architecture du Projet](#architecture-du-projet)
- [Pages et Routes](#pages-et-routes)
- [Composants](#composants)
- [SEO et Référencement](#seo-et-référencement)
- [Sécurité Frontend](#sécurité-frontend)
- [Build de Production](#build-de-production)
- [Scripts Disponibles](#scripts-disponibles)

---

## Aperçu

Le site est un **site vitrine institutionnel** pensé pour présenter l'activité de Coreline Alliance auprès d'investisseurs, partenaires et institutions. Il comprend :

- Une page d'accueil dynamique avec animations et métriques d'impact
- La présentation des services et solutions de l'alliance
- Un portfolio de projets / missions
- Une section actualités et insights
- Un formulaire de contact professionnel relié à l'API backend
- Des pages légales (mentions légales, politique de confidentialité)
- Un design responsive mobile-first avec animations fluides

---

## Stack Technique

| Technologie                     | Version | Rôle                                               |
| ------------------------------- | ------- | -------------------------------------------------- |
| **React**                       | 19.0.0  | Bibliothèque UI                                    |
| **Vite**                        | 6.2.0   | Bundler et serveur de développement                |
| **React Router**                | 7.14.1  | Navigation SPA                                     |
| **Framer Motion**               | 12.6.2  | Animations et transitions                          |
| **Lucide React**                | 1.8.0   | Icônes SVG                                         |
| **React Icons**                 | 5.5.0   | Bibliothèque d'icônes complémentaire               |
| **React Helmet Async**          | 3.0.0   | Gestion dynamique des meta tags SEO                |
| **React CountUp**               | 6.5.3   | Animations de compteurs numériques                 |
| **React Intersection Observer** | 10.0.3  | Détection de visibilité pour lazy-loading          |
| **Vanilla CSS**                 | —       | Fichier `coreline.css` unique pour tout le styling |
| **ESLint**                      | 9.21.0  | Linting du code                                    |

---

## Prérequis

- **Node.js 18+** et **npm**
- Le [backend FastAPI](../server/README.md) en fonctionnement (pour le formulaire de contact)

---

## Installation

### 1. Se placer dans le dossier client

```bash
cd client
```

### 2. Installer les dépendances

```bash
npm install
```

---

## Configuration

### Variables d'environnement

Copier le fichier modèle et le personnaliser :

```bash
cp .env.example .env
```

| Variable       | Description            | Valeur par défaut       |
| -------------- | ---------------------- | ----------------------- |
| `VITE_API_URL` | URL du backend FastAPI | `http://localhost:8000` |

### Exemple `.env`

```env
VITE_API_URL=http://localhost:8000
```

> **Note :** Les variables Vite doivent être préfixées par `VITE_` pour être accessibles côté client via `import.meta.env`.

---

## Lancement

### Développement

```bash
npm run dev
```

Le serveur de développement démarre sur **http://localhost:5173** avec hot-reload activé.

### Prévisualisation du build

```bash
npm run build
npm run preview
```

---

## Architecture du Projet

```
client/
├── public/
│   ├── assets/              # Images et logos du site
│   ├── images/              # Images supplémentaires
│   ├── robots.txt           # Règles pour les crawlers
│   └── sitemap.xml          # Plan du site pour le SEO
├── src/
│   ├── main.jsx             # Point d'entrée — React + BrowserRouter + HelmetProvider
│   ├── App.jsx              # Routeur principal et layout (Navbar + Routes + Footer)
│   ├── coreline.css         # Feuille de styles globale unique
│   ├── components/
│   │   ├── common/
│   │   │   └── SEO.jsx      # Composant SEO réutilisable (meta tags dynamiques)
│   │   ├── home/
│   │   │   ├── Hero.jsx             # Bannière d'accueil
│   │   │   ├── BentoServices.jsx    # Grille de services style bento
│   │   │   ├── MissionSection.jsx   # Section mission de l'alliance
│   │   │   ├── ImpactMetrics.jsx    # Compteurs animés (impact)
│   │   │   ├── Portfolio.jsx        # Projets et portfolio
│   │   │   ├── TeamSection.jsx      # Présentation de l'équipe
│   │   │   ├── CeoWord.jsx          # Mot du dirigeant
│   │   │   ├── NewsSection.jsx      # Aperçu des actualités
│   │   │   └── ContactSection.jsx   # Section contact en bas de page
│   │   └── layout/
│   │       ├── Navbar.jsx           # Barre de navigation responsive
│   │       └── Footer.jsx           # Pied de page
│   └── pages/
│       ├── Home.jsx                     # Page d'accueil
│       ├── AboutPage.jsx                # Page « À propos »
│       ├── ServicePage.jsx              # Page des services
│       ├── SolutionsPage.jsx            # Page solutions / portfolio
│       ├── ContactPage.jsx              # Page contact avec formulaire
│       ├── NewsPage.jsx                 # Liste des actualités
│       ├── NewsDetailPage.jsx           # Détail d'un article
│       ├── ProduitDetailPage.jsx        # Détail d'un produit
│       ├── MentionsLegales.jsx          # Mentions légales
│       ├── PolitiqueConfidentialite.jsx # Politique de confidentialité
│       ├── ComingSoon.jsx               # Page « Bientôt disponible »
│       └── NotFound.jsx                 # Page 404
├── index.html           # HTML d'entrée avec meta tags SEO et CSP
├── vite.config.js       # Configuration Vite
├── eslint.config.js     # Configuration ESLint
├── package.json         # Dépendances et scripts
├── .env                 # Variables d'environnement (ignoré par git)
└── .env.example         # Modèle de configuration
```

---

## Pages et Routes

| Route                        | Page                       | Description                               |
| ---------------------------- | -------------------------- | ----------------------------------------- |
| `/`                          | `Home`                     | Page d'accueil avec toutes les sections   |
| `/about`                     | `AboutPage`                | Présentation de l'alliance et de l'équipe |
| `/services`                  | `ServicePage`              | Détail des services proposés              |
| `/solutions`                 | `ComingSoon`               | Portfolio des missions _(à venir)_        |
| `/solutions/:id`             | `ComingSoon`               | Détail d'un projet _(à venir)_            |
| `/actualites`                | `ComingSoon`               | Liste des actualités _(à venir)_          |
| `/actualites/:id`            | `ComingSoon`               | Détail d'un article _(à venir)_           |
| `/contact`                   | `ContactPage`              | Formulaire de contact                     |
| `/mentions-legales`          | `MentionsLegales`          | Mentions légales                          |
| `/politique-confidentialite` | `PolitiqueConfidentialite` | Politique de confidentialité              |
| `*`                          | `NotFound`                 | Page 404                                  |

> **Note :** Les pages marquées _« à venir »_ affichent un composant `ComingSoon` en attendant leur implémentation complète.

---

## Composants

### Layout

- **`Navbar`** — Navigation responsive avec menu burger mobile. Liens vers toutes les sections principales.
- **`Footer`** — Pied de page avec liens utiles, informations de contact et copyright.

### Home (sections de la page d'accueil)

| Composant        | Description                                  |
| ---------------- | -------------------------------------------- |
| `Hero`           | Bannière principale avec titre et CTA        |
| `BentoServices`  | Grille de services au format « bento grid »  |
| `MissionSection` | Présentation de la mission de l'alliance     |
| `ImpactMetrics`  | Compteurs animés (chiffres clés de l'impact) |
| `Portfolio`      | Aperçu des projets et missions               |
| `TeamSection`    | Présentation des membres de l'équipe         |
| `CeoWord`        | Citation / mot du fondateur                  |
| `NewsSection`    | Dernières actualités                         |
| `ContactSection` | Mini formulaire de contact / CTA             |

### Common

- **`SEO`** — Composant réutilisable qui injecte dynamiquement les balises `<title>`, Open Graph et Twitter Card via `react-helmet-async`.

---

## SEO et Référencement

Le site implémente une stratégie SEO complète :

| Élément                     | Implémentation                                                    |
| --------------------------- | ----------------------------------------------------------------- |
| **Meta tags dynamiques**    | Composant `SEO.jsx` avec Helmet Async sur chaque page             |
| **Open Graph**              | Tags OG pour Facebook et LinkedIn                                 |
| **Twitter Cards**           | Tags `summary_large_image` pour Twitter                           |
| **Content Security Policy** | CSP stricte définie dans `index.html`                             |
| **Sitemap XML**             | `public/sitemap.xml` — plan du site pour les moteurs de recherche |
| **robots.txt**              | `public/robots.txt` — autorise l'indexation complète              |
| **Favicon**                 | Logo Coreline en format PNG                                       |
| **Theme Color**             | `#cda141` (doré Coreline)                                         |
| **Langue**                  | `<html lang="fr">`                                                |

---

## Sécurité Frontend

| Mécanisme                         | Description                                                                                                                                                                       |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Content Security Policy (CSP)** | Politique restrictive dans `index.html` : scripts `self` uniquement, styles limités à `self` + Google Fonts, images limitées à `self` + Unsplash, connexions à `self` + Formspree |
| **Referrer Policy**               | `strict-origin-when-cross-origin`                                                                                                                                                 |
| **X-Content-Type-Options**        | `nosniff`                                                                                                                                                                         |
| **Permissions Policy**            | Caméra, microphone et géolocalisation désactivés                                                                                                                                  |
| **Frame Ancestors**               | `'none'` — empêche l'intégration en iframe                                                                                                                                        |
| **Honeypot anti-spam**            | Champ caché `website` dans le formulaire de contact                                                                                                                               |
| **Validation côté client**        | Regex email + champs obligatoires avant envoi au backend                                                                                                                          |
| **Console stripping**             | `console.log` et `debugger` supprimés en build de production via esbuild                                                                                                          |

---

## Build de Production

```bash
npm run build
```

Le build optimisé est généré dans le dossier `dist/`. Il est prêt à être servi par n'importe quel serveur web statique.

### Optimisations Vite

- **Minification** via esbuild
- **Suppression automatique** des `console` et `debugger` en production
- **Tree-shaking** complet

---

## Scripts Disponibles

| Commande          | Description                                   |
| ----------------- | --------------------------------------------- |
| `npm run dev`     | Lance le serveur de développement (port 5173) |
| `npm run build`   | Génère le build de production dans `dist/`    |
| `npm run preview` | Prévisualise le build de production           |
| `npm run lint`    | Vérifie le code avec ESLint                   |

---

## Support

Pour toute question technique, contactez l'équipe de développement **Coreline Alliance**.
