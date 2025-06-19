import React, { useState, useMemo, useEffect } from 'react';

// Icônes SVG simples intégrées
const Icons = {
  Search: () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
    </svg>
  ),
  Code: () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  ),
  Database: () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
      <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
      <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
      <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
    </svg>
  ),
  Web: () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clipRule="evenodd" />
    </svg>
  ),
  Cloud: () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
      <path d="M5.5 16a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 16h-8z" />
    </svg>
  )
};

const HomePage = ({ onSelectTech }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [technologies, setTechnologies] = useState([]);
  const [loading, setLoading] = useState(true);

  // Récupérer les technologies depuis l'API
  useEffect(() => {
    const fetchTechnologies = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/technologies`);
        if (response.ok) {
          const data = await response.json();
          setTechnologies(data);
        } else {
          console.error('Failed to fetch technologies');
        }
      } catch (error) {
        console.error('Error fetching technologies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTechnologies();
  }, []);

  // Technologies statiques comme fallback
  const staticTechnologies = {
    frontend: [
      { name: 'React', icon: 'react', color: '#61DAFB' },
      { name: 'Angular', icon: 'angular', color: '#DD0031' },
      { name: 'Vue.js', icon: 'vue', color: '#4FC08D' },
      { name: 'JavaScript', icon: 'javascript', color: '#F7DF1E' },
      { name: 'TypeScript', icon: 'typescript', color: '#3178C6' },
    ],
    backend: [
      { name: 'Python', icon: 'python', color: '#3776AB' },
      { name: 'Node.js', icon: 'nodejs', color: '#339933' },
      { name: 'Java', icon: 'java', color: '#007396' },
      { name: 'PHP', icon: 'php', color: '#777BB4' },
      { name: 'C#', icon: 'csharp', color: '#239120' },
    ],
    database: [
      { name: 'MySQL', icon: 'mysql', color: '#4479A1' },
      { name: 'MongoDB', icon: 'mongodb', color: '#47A248' },
      { name: 'PostgreSQL', icon: 'postgresql', color: '#336791' },
      { name: 'Redis', icon: 'redis', color: '#DC382D' },
    ],
    cloud: [
      { name: 'AWS', icon: 'aws', color: '#232F3E' },
      { name: 'Docker', icon: 'docker', color: '#2496ED' },
      { name: 'Kubernetes', icon: 'kubernetes', color: '#326CE5' },
      { name: 'Azure', icon: 'azure', color: '#0089D6' },
    ]
  };

  const categories = [
    { id: 'all', name: 'Toutes', icon: <Icons.Code /> },
    { id: 'frontend', name: 'Frontend', icon: <Icons.Web /> },
    { id: 'backend', name: 'Backend', icon: <Icons.Database /> },
    { id: 'database', name: 'Base de données', icon: <Icons.Database /> },
    { id: 'cloud', name: 'Cloud & DevOps', icon: <Icons.Cloud /> }
  ];

  const filteredTechnologies = useMemo(() => {
    let techs = [];
    
    // Utiliser les technologies de l'API si disponibles, sinon les statiques
    if (technologies.length > 0) {
      // Technologies depuis l'API
      techs = technologies.map(tech => ({
        name: tech.display_name || tech.name,
        originalName: tech.name,
        icon: tech.icon || '💻',
        color: tech.color || '#007bff'
      }));
    } else {
      // Technologies statiques
      if (activeCategory === 'all') {
        Object.values(staticTechnologies).forEach(categoryTechs => {
          techs = [...techs, ...categoryTechs];
        });
      } else {
        techs = staticTechnologies[activeCategory] || [];
      }
    }

    // Filtrer selon le terme de recherche
    return techs.filter(tech => 
      tech.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [searchTerm, activeCategory, technologies]);

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* Barre de recherche */}
      <div className="relative mb-8">
        <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
          <Icons.Search />
        </div>
        <input
          type="search"
          placeholder="Rechercher une technologie..."
          className="w-full pl-12 pr-4 py-3 rounded-lg border bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Catégories */}
      <div className="flex gap-4 mb-8 overflow-x-auto pb-2">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => setActiveCategory(category.id)}
            className={`flex items-center px-4 py-2 rounded-full transition-colors ${
              activeCategory === category.id
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            <span className="mr-2">{category.icon}</span>
            {category.name}
          </button>
        ))}
      </div>

      {/* Grille des technologies */}
      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-2 text-gray-500">Chargement des technologies...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredTechnologies.map(tech => (
            <button
              key={tech.originalName || tech.name}
              onClick={() => onSelectTech(tech.originalName || tech.name)}
              className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              <span className="font-medium text-gray-800">{tech.name}</span>
            </button>
          ))}
        </div>
      )}

      {/* Message si aucun résultat */}
      {filteredTechnologies.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          Aucune technologie trouvée pour "{searchTerm}"
        </div>
      )}
    </div>
  );
};

export default HomePage; 