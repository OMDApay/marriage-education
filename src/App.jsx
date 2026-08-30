import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Heart, Users, BookOpen, Shield, HelpCircle, Star, Search, Settings, Grid, FileText, Eye, AlertTriangle } from 'lucide-react'
import PositionCard from '@/components/PositionCard.jsx'
import PositionModal from '@/components/PositionModal.jsx'
import AdminPanel from '@/components/AdminPanel.jsx'
import AdSpace from '@/components/AdSpace.jsx'
import ArticleCard from '@/components/ArticleCard.jsx'
import ArticleModal from '@/components/ArticleModal.jsx'
import { sexualPositions, searchPositions, getPositionsByCategory } from '@/data/positions.js'
import { articles, chapters, searchArticles, getArticlesByCategory, getArticlesForSection } from '@/data/articles.js'
import sexualDiseasesChapter from '@/data/sexualDiseases.js'
import pornMediaLiteracyChapter from '@/data/pornMediaLiteracy.js'
import tragedyChapter from '@/data/tragedyChapter.js'
import './App.css'
import { assetPath } from '@/lib/assetPath.js'

// Import images
import maleReproductiveAr from './assets/male_reproductive_system_ar.jpg'
import femaleReproductiveAr from './assets/female_reproductive_system_ar.jpg'
import headerImg from './assets/header.jpg'

function App() {
  const [activeSection, setActiveSection] = useState('home')
  const [selectedPosition, setSelectedPosition] = useState(null)
  const [isPositionModalOpen, setIsPositionModalOpen] = useState(false)
  const [selectedArticle, setSelectedArticle] = useState(null)
  const [isArticleModalOpen, setIsArticleModalOpen] = useState(false)
  const [isAdminPanelOpen, setIsAdminPanelOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [articleSearchQuery, setArticleSearchQuery] = useState('')
  const [selectedChapter, setSelectedChapter] = useState(null)
  const [ageVerified, setAgeVerified] = useState(() => localStorage.getItem('marriage_age_verified') === 'true')

  // حماية الموقع من أيقونة Edit Mode المزعجة
  useEffect(() => {
    const hideEditMode = () => {
      const selectors = [
        '[data-edit-mode]', '.edit-mode', '.edit-mode-button', 
        'button[title*="Edit"]', 'button[aria-label*="Edit"]',
        '.manus-edit-mode', '#edit-mode', '.edit-toolbar'
      ];
      selectors.forEach(s => {
        document.querySelectorAll(s).forEach(el => {
          el.style.display = 'none';
          el.style.visibility = 'hidden';
          el.remove(); // إزالة العنصر تماماً
        });
      });
      
      // البحث عن الأزرار التي تحتوي على نص "Edit mode"
      document.querySelectorAll('button').forEach(btn => {
        if (btn.textContent.includes('Edit mode') || btn.textContent.includes('تحرير')) {
          btn.remove();
        }
      });
    };

    hideEditMode();
    const interval = setInterval(hideEditMode, 1000); // تكرار كل ثانية للتأكد
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const chapterMeta = {
      pornMediaLiteracy: pornMediaLiteracyChapter,
      tragedy: tragedyChapter,
      sexualDiseases: sexualDiseasesChapter,
    }[activeSection]
    const title = selectedArticle?.title || chapterMeta?.title || 'دليل التثقيف الزواجي'
    const description = selectedArticle?.description || chapterMeta?.subtitle || 'محتوى تثقيفي صحي وزواجي محترم باللغة العربية.'
    document.title = `${title} | دليل التثقيف الزواجي`
    let meta = document.querySelector('meta[name="description"]')
    if (!meta) { meta = document.createElement('meta'); meta.name = 'description'; document.head.appendChild(meta) }
    meta.content = description
  }, [activeSection, selectedArticle])

  const sections = [
    { id: 'home', title: 'الرئيسية', icon: Heart },
    { id: 'intro', title: 'مقدمة', icon: BookOpen },
    { id: 'anatomy', title: 'التشريح', icon: Users },
    { id: 'positions', title: 'الأوضاع', icon: Grid },
    { id: 'articles', title: 'المقالات', icon: FileText },
    { id: 'sexualDiseases', title: 'الأمراض الجنسية', icon: Shield },
    { id: 'pornMediaLiteracy', title: 'لا تصدّق الإباحية', icon: Eye },
    { id: 'tragedy', title: 'نهاية مأساوية', icon: AlertTriangle },
    { id: 'tips', title: 'النصائح', icon: Star },
    { id: 'faq', title: 'الأسئلة', icon: HelpCircle }
  ]

  const positionCategories = [
    { id: 'all', title: 'جميع الأوضاع' },
    { id: 'أوضاع الوقوف', title: 'أوضاع الوقوف' },
    { id: 'أوضاع الجلوس', title: 'أوضاع الجلوس' },
    { id: 'أوضاع متقدمة', title: 'أوضاع متقدمة' },
    { id: 'أوضاع رومانسية', title: 'أوضاع رومانسية' }
  ]

  const handleViewPositionDetails = (position) => {
    setSelectedPosition(position)
    setIsPositionModalOpen(true)
  }

  const handleViewArticleDetails = (article) => {
    setSelectedArticle(article)
    setIsArticleModalOpen(true)
  }

  const getFilteredPositions = () => {
    let filtered = sexualPositions
    if (selectedCategory !== 'all') filtered = getPositionsByCategory(selectedCategory)
    if (searchQuery) {
      filtered = searchPositions(searchQuery).filter(p => 
        selectedCategory === 'all' || p.category === selectedCategory
      )
    }
    return filtered
  }

  const getFilteredArticles = () => {
    if (articleSearchQuery) return searchArticles(articleSearchQuery)
    return articles
  }

  if (!ageVerified) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-rose-950 flex items-center justify-center p-6 font-arabic" dir="rtl">
        <Card className="max-w-xl w-full border-white/20 bg-white/95 shadow-2xl rounded-3xl overflow-hidden">
          <div className="h-3 bg-gradient-to-l from-rose-500 via-pink-500 to-indigo-600" />
          <CardContent className="p-8 md:p-12 text-center">
            <div className="mx-auto mb-6 h-16 w-16 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center"><Shield className="h-9 w-9" /></div>
            <h1 className="text-3xl font-bold text-slate-900 mb-4">تنبيه عمر ومحتوى تثقيفي</h1>
            <p className="text-slate-700 leading-8 mb-4">هذا الموقع مخصص للبالغين بعمر <strong>18 عاماً أو أكثر</strong>، ويقدم تثقيفاً صحياً وزوجياً محترماً. لا يحتوي على مواد إباحية، لكنه يناقش موضوعات حساسة عن الصحة الجنسية والعلاقات.</p>
            <p className="text-sm text-slate-500 leading-7 mb-8">بالضغط على «أوافق» تؤكد أن عمرك 18 عاماً أو أكثر وأنك ترغب في متابعة محتوى تثقيفي للبالغين. لا يُعد هذا التحقق وسيلة قانونية لإثبات العمر.</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button className="bg-rose-600 hover:bg-rose-700 text-white rounded-xl px-6 py-6 text-base" onClick={() => { localStorage.setItem('marriage_age_verified', 'true'); setAgeVerified(true) }}>أوافق، عمري 18 عاماً أو أكثر</Button>
              <Button variant="outline" className="rounded-xl px-6 py-6 text-base" onClick={() => document.body.innerHTML = '<div dir="rtl" style="font-family:sans-serif;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center;padding:24px"><div><h1>لم يتم الدخول إلى الموقع</h1><p>يمكنك إغلاق هذه الصفحة الآن.</p></div></div>'}>لا، أريد الخروج</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-pink-50 font-arabic" dir="rtl">
      {/* إعلان الرأس */}
      <AdSpace location="header" className="w-full" />
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => setActiveSection('home')}>
              <div className="bg-pink-500 p-2 rounded-lg">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-l from-pink-600 to-blue-600 bg-clip-text text-transparent">
                دليل التثقيف الزواجي
              </h1>
            </div>
            <div className="flex items-center gap-2 md:gap-4">
              <nav className="hidden xl:flex space-x-2 space-x-reverse">
                {sections.map((section) => {
                  const Icon = section.icon
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id)}
                      className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all ${
                        activeSection === section.id
                          ? 'bg-pink-500 text-white shadow-md'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      <span className="font-medium">{section.title}</span>
                    </button>
                  )
                })}
              </nav>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsAdminPanelOpen(true)}
                className="text-gray-400 hover:text-gray-600 rounded-full"
              >
                <Settings className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <div className="xl:hidden bg-white border-t sticky top-[64px] z-40 overflow-x-auto">
        <div className="flex p-2 gap-2 min-w-max">
          {sections.map((section) => {
            const Icon = section.icon
            return (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-full whitespace-nowrap transition-all ${
                  activeSection === section.id
                    ? 'bg-pink-500 text-white shadow-sm'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span className="text-sm font-medium">{section.title}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1">
            {activeSection === 'home' && (
              <div className="space-y-12">
                {/* Hero image — the supplied header artwork is shown without any color overlay */}
                <section className="rounded-3xl overflow-hidden bg-white shadow-xl border border-white">
                  <img
                    src={headerImg}
                    alt="دليل التثقيف الزواجي"
                    className="block w-full h-auto max-h-[620px] object-cover object-center"
                  />
                </section>

                {/* Intro and actions below the image, keeping the supplied artwork unobstructed */}
                <section className="text-center space-y-5 py-2 md:py-4">
                  <h2 className="text-3xl md:text-5xl font-bold leading-tight text-gray-900">
                    رحلتكم نحو حياة زوجية سعيدة تبدأ هنا
                  </h2>
                  <p className="max-w-3xl mx-auto text-lg md:text-xl text-gray-600">
                    أكبر موسوعة عربية للتثقيف الزواجي والصحة الجنسية، مقدمة بطريقة علمية، محترمة، وشاملة.
                  </p>
                  <div className="flex flex-wrap gap-4 justify-center">
                    <Button
                      onClick={() => setActiveSection('positions')}
                      className="bg-pink-500 text-white hover:bg-pink-600 px-8 py-6 text-lg rounded-xl font-bold shadow-lg"
                    >
                      استكشف 50 وضعاً جنسياً
                    </Button>
                    <Button
                      onClick={() => setActiveSection('articles')}
                      className="bg-blue-600 text-white hover:bg-blue-700 px-8 py-6 text-lg rounded-xl font-bold shadow-lg"
                    >
                      استعرض المقالات المتخصصة
                    </Button>
                  </div>
                </section>

                {/* Quick Stats */}
                <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { label: 'وضع جنسي مصور', value: '50+', color: 'bg-pink-100 text-pink-600' },
                    { label: 'مقالة طبية متخصصة', value: '200+', color: 'bg-blue-100 text-blue-600' },
                    { label: 'دليل شامل للعرسان', value: '100%', color: 'bg-green-100 text-green-600' },
                    { label: 'خصوصية وأمان تام', value: '🔒', color: 'bg-purple-100 text-purple-600' }
                  ].map((stat, i) => (
                    <div key={i} className={`${stat.color} p-6 rounded-2xl text-center shadow-sm`}>
                      <div className="text-3xl font-bold mb-1">{stat.value}</div>
                      <div className="text-sm font-medium opacity-80">{stat.label}</div>
                    </div>
                  ))}
                </section>

                <AdSpace location="between_sections" className="my-8" />

                {/* Latest Articles Snippet */}
                <section className="space-y-6">
                  <div className="flex justify-between items-end">
                    <h3 className="text-2xl font-bold text-gray-800">أحدث المقالات التعليمية</h3>
                    <Button variant="link" onClick={() => setActiveSection('articles')} className="text-blue-600">عرض الكل</Button>
                  </div>
                  <div className="grid md:grid-cols-3 gap-6">
                    {articles.slice(0, 3).map(article => (
                      <ArticleCard key={article.id} article={article} onViewDetails={handleViewArticleDetails} />
                    ))}
                  </div>
                </section>
              </div>
            )}

            {activeSection === 'intro' && (
              <div className="max-w-4xl mx-auto space-y-8">
                <Card className="border-none shadow-xl rounded-3xl overflow-hidden">
                  <div className="bg-blue-600 p-8 text-white text-center">
                    <h2 className="text-3xl font-bold">مقدمة في الحياة الزوجية</h2>
                    <p className="mt-2 opacity-90">الأساس المتين لعلاقة تدوم مدى الحياة</p>
                  </div>
                  <CardContent className="p-8 prose prose-lg max-w-none text-right">
                    <p className="text-xl leading-relaxed text-gray-700">
                      الزواج هو أسمى الروابط الإنسانية، وهو رحلة مشتركة تتطلب الوعي، الصبر، والتعلم المستمر. في هذا القسم، نستعرض المفاهيم الأساسية التي تجعل من الزواج سكناً ومودة.
                    </p>
                    
                    <div className="grid md:grid-cols-2 gap-6 my-8 not-prose">
                      {getArticlesForSection('intro').map(article => (
                        <div key={article.id} className="bg-gray-50 p-4 rounded-xl border-r-4 border-blue-500 cursor-pointer hover:bg-blue-50 transition-colors" onClick={() => handleViewArticleDetails(article)}>
                          <h4 className="font-bold text-blue-800">{article.title}</h4>
                          <p className="text-sm text-gray-600 line-clamp-2 mt-1">{article.description}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeSection === 'anatomy' && (
              <div className="max-w-4xl mx-auto space-y-8">
                <Card className="border-none shadow-xl rounded-3xl overflow-hidden">
                  <div className="bg-green-600 p-8 text-white text-center">
                    <h2 className="text-3xl font-bold">التشريح والفسيولوجيا</h2>
                    <p className="mt-2 opacity-90">افهم جسدك وجسد شريكك من منظور طبي</p>
                  </div>
                  <CardContent className="p-8">
                    <Tabs defaultValue="male" className="w-full" dir="rtl">
                      <TabsList className="grid w-full grid-cols-2 mb-8 bg-gray-100 p-1 rounded-xl">
                        <TabsTrigger value="male" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm py-3">الجهاز التناسلي الذكري</TabsTrigger>
                        <TabsTrigger value="female" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm py-3">الجهاز التناسلي الأنثوي</TabsTrigger>
                      </TabsList>
                      
                      <TabsContent value="male" className="space-y-8">
                        <img src={maleReproductiveAr} alt="التشريح الذكري" className="w-full rounded-2xl shadow-lg" />
                        <div className="grid md:grid-cols-2 gap-4">
                          {getArticlesForSection('anatomy').slice(0, 4).map(article => (
                            <Card key={article.id} className="cursor-pointer hover:border-green-500 transition-all" onClick={() => handleViewArticleDetails(article)}>
                              <CardHeader className="p-4">
                                <CardTitle className="text-base">{article.title}</CardTitle>
                              </CardHeader>
                            </Card>
                          ))}
                        </div>
                      </TabsContent>

                      <TabsContent value="female" className="space-y-8">
                        <img src={femaleReproductiveAr} alt="التشريح الأنثوي" className="w-full rounded-2xl shadow-lg" />
                        <div className="grid md:grid-cols-2 gap-4">
                          {getArticlesForSection('anatomy').slice(4, 8).map(article => (
                            <Card key={article.id} className="cursor-pointer hover:border-pink-500 transition-all" onClick={() => handleViewArticleDetails(article)}>
                              <CardHeader className="p-4">
                                <CardTitle className="text-base">{article.title}</CardTitle>
                              </CardHeader>
                            </Card>
                          ))}
                        </div>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeSection === 'positions' && (
              <div className="space-y-8">
                <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                  <div className="text-center max-w-2xl mx-auto mb-8 space-y-4">
                    <h2 className="text-3xl font-bold text-gray-800">دليل الأوضاع الـ 50 الشامل</h2>
                    <p className="text-gray-600">مجموعة مختارة بعناية لتناسب جميع الأذواق والمستويات، مع شرح طبي وفني لكل وضع.</p>
                  </div>

                  <div className="flex flex-col md:flex-row gap-4 mb-8">
                    <div className="flex-1 relative">
                      <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <Input 
                        placeholder="ابحث عن وضع معين (مثلاً: كلاسيكي، عميق...)" 
                        className="pr-12 py-6 rounded-xl border-gray-200"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                      />
                    </div>
                    <select 
                      className="bg-gray-50 border border-gray-200 rounded-xl px-6 py-3 font-medium"
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                      {positionCategories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.title}</option>
                      ))}
                    </select>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {getFilteredPositions().map(pos => (
                      <PositionCard key={pos.id} position={pos} onViewDetails={handleViewPositionDetails} />
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeSection === 'articles' && (
              <div className="space-y-8">
                <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                  <div className="text-center max-w-2xl mx-auto mb-8 space-y-4">
                    <h2 className="text-3xl font-bold text-gray-800">موسوعة المقالات المتخصصة (200 مقالة)</h2>
                    <p className="text-gray-600">دليل شامل يغطي الجوانب الطبية، النفسية، والاجتماعية للحياة الزوجية، مقسمة إلى أبواب متخصصة.</p>
                  </div>

                  <div className="relative mb-8">
                    <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <Input 
                      placeholder="ابحث في 200 مقالة طبية..." 
                      className="pr-12 py-6 rounded-xl border-gray-200"
                      value={articleSearchQuery}
                      onChange={(e) => {
                        setArticleSearchQuery(e.target.value)
                        if (e.target.value) setSelectedChapter(null)
                      }}
                    />
                  </div>

                  {articleSearchQuery ? (
                    <div>
                      <h3 className="text-xl font-bold text-gray-800 mb-6">نتائج البحث ({getFilteredArticles().length})</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        {getFilteredArticles().map(article => (
                          <ArticleCard key={article.id} article={article} onViewDetails={handleViewArticleDetails} />
                        ))}
                      </div>
                    </div>
                  ) : !selectedChapter ? (
                    <div>
                      <h3 className="text-xl font-bold text-gray-800 mb-6">أبواب الموسوعة (اضغط على أي باب لاستعراض مقالاته)</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {chapters.map(chapter => (
                          <Card 
                            key={chapter.id} 
                            className="overflow-hidden hover:shadow-xl transition-all cursor-pointer border border-gray-100 group flex flex-col"
                            onClick={() => setSelectedChapter(chapter)}
                          >
                            <div className="relative h-48 overflow-hidden">
                              <img 
                                src={assetPath(chapter.image)} 
                                alt={chapter.title} 
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
                              <span className="absolute bottom-4 right-4 bg-pink-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                                {chapter.count} مقالة
                              </span>
                            </div>
                            <CardHeader className="p-6 flex-1 flex flex-col justify-between">
                              <div>
                                <CardTitle className="text-xl font-bold text-gray-800 group-hover:text-pink-600 transition-colors mb-2">
                                  {chapter.title}
                                </CardTitle>
                                <CardDescription className="text-gray-600 text-sm line-clamp-2">
                                  {chapter.description}
                                </CardDescription>
                              </div>
                              <div className="mt-4 flex items-center text-pink-600 font-bold text-sm gap-2">
                                <span>استعراض مقالات الباب</span>
                                <span>←</span>
                              </div>
                            </CardHeader>
                          </Card>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6 bg-blue-50 p-6 rounded-2xl gap-4">
                        <div>
                          <h3 className="text-2xl font-bold text-blue-900">{selectedChapter.title}</h3>
                          <p className="text-blue-700 text-sm mt-1">{selectedChapter.description}</p>
                        </div>
                        <Button 
                          onClick={() => setSelectedChapter(null)}
                          className="bg-pink-600 text-white hover:bg-pink-500 px-6 py-4 rounded-xl font-bold shadow-md flex items-center gap-2"
                        >
                          <Grid className="h-5 w-5" />
                          <span>العودة لقائمة الأبواب الرئيسية</span>
                        </Button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                        {getArticlesByCategory(selectedChapter.title).map(article => (
                          <ArticleCard key={article.id} article={article} onViewDetails={handleViewArticleDetails} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeSection === 'sexualDiseases' && (
              <div className="space-y-8">
                <Card className="overflow-hidden border-none shadow-xl rounded-3xl">
                  <div className="relative h-64 md:h-80 overflow-hidden">
                    <img
                      src={assetPath(sexualDiseasesChapter.image)}
                      alt="الأمراض الجنسية: التوعية والوقاية"
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/25 to-transparent" />
                    <div className="absolute bottom-6 right-6 left-6 text-white">
                      <div className="flex items-center gap-2 text-sm font-bold mb-2"><Shield className="h-5 w-5" /> باب تثقيفي جديد</div>
                      <h2 className="text-3xl md:text-4xl font-bold">{sexualDiseasesChapter.title}</h2>
                      <p className="mt-2 text-white/90">{sexualDiseasesChapter.subtitle}</p>
                    </div>
                  </div>
                  <CardContent className="p-6 md:p-8">
                    <div className="bg-amber-50 border-r-4 border-amber-400 p-4 rounded-xl text-amber-900 leading-relaxed mb-8">
                      <strong>تنبيه مهم:</strong> هذا الباب للتوعية العامة، ولا يُستخدم للتشخيص أو وصف العلاج. عند وجود أعراض أو تعرض محتمل، يجب مراجعة طبيب أو مركز صحي موثوق مع الحفاظ على الخصوصية.
                    </div>
                    <div className="flex items-center justify-between gap-4 mb-6">
                      <div>
                        <h3 className="text-2xl font-bold text-gray-800">موضوعات الباب</h3>
                        <p className="text-gray-600 mt-1">تعريف العدوى، الأعراض، الفحوصات، الوقاية، والعلاج الطبي المسؤول.</p>
                      </div>
                      <span className="shrink-0 bg-pink-100 text-pink-700 px-3 py-2 rounded-full text-sm font-bold">10 مقالات</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                      {sexualDiseasesChapter.articles.map(article => (
                        <ArticleCard
                          key={article.id}
                          article={{ ...article, category: sexualDiseasesChapter.title }}
                          onViewDetails={handleViewArticleDetails}
                        />
                      ))}
                    </div>
                    <div className="mt-8 pt-6 border-t border-gray-100 text-sm text-gray-600 leading-relaxed">
                      {sexualDiseasesChapter.sourceNote} وقد تمت مراجعة الصياغة لتجنب التخويف والوصمة، مع التأكيد على أهمية الفحص والعلاج لدى المختصين.
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeSection === 'pornMediaLiteracy' && (
              <div className="space-y-8">
                <Card className="overflow-hidden border-none shadow-xl rounded-3xl">
                  <div className="relative h-64 md:h-80 overflow-hidden">
                    <img src={assetPath(pornMediaLiteracyChapter.image)} alt="لا تصدّق الأفلام الإباحية" className="w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent" />
                    <div className="absolute bottom-6 right-6 left-6 text-white">
                      <div className="flex items-center gap-2 text-sm font-bold mb-2"><Eye className="h-5 w-5" /> وعي إعلامي وتثقيف زوجي</div>
                      <h2 className="text-3xl md:text-4xl font-bold">{pornMediaLiteracyChapter.title}</h2>
                      <p className="mt-2 text-white/90">{pornMediaLiteracyChapter.subtitle}</p>
                    </div>
                  </div>
                  <CardContent className="p-6 md:p-8">
                    <div className="bg-violet-50 border-r-4 border-violet-400 p-4 rounded-xl text-violet-900 leading-relaxed mb-8">
                      <strong>رسالة الباب:</strong> المشاهد المصورة للبالغين ليست مرجعاً طبياً أو دليلاً للحياة الزوجية. العلاقة الصحية تقوم على المعرفة والموافقة والخصوصية والحوار، لا على تقليد الأداء أمام الكاميرا.
                    </div>
                    <div className="flex items-center justify-between gap-4 mb-6">
                      <div>
                        <h3 className="text-2xl font-bold text-gray-800">موضوعات الباب</h3>
                        <p className="text-gray-600 mt-1">قراءة نقدية هادئة للتمثيل والمونتاج والتوقعات والموافقة والتواصل.</p>
                      </div>
                      <span className="shrink-0 bg-violet-100 text-violet-700 px-3 py-2 rounded-full text-sm font-bold">10 مقالات</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                      {pornMediaLiteracyChapter.articles.map(article => (
                        <ArticleCard key={article.id} article={{ ...article, category: pornMediaLiteracyChapter.title }} onViewDetails={handleViewArticleDetails} />
                      ))}
                    </div>
                    <div className="mt-8 pt-6 border-t border-gray-100 text-sm text-gray-600 leading-relaxed">
                      {pornMediaLiteracyChapter.sourceNote} ويُنصح بطلب دعم مختص عند وجود ضيق مستمر أو فقدان سيطرة أو تأثير واضح في النوم والعمل والعلاقة.
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeSection === 'tragedy' && (
              <div className="space-y-8">
                <Card className="overflow-hidden border-none shadow-xl rounded-3xl">
                  <div className="relative h-64 md:h-80 overflow-hidden">
                    <img src={assetPath(tragedyChapter.image)} alt={tragedyChapter.title} className="w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/25 to-transparent" />
                    <div className="absolute bottom-6 right-6 left-6 text-white">
                      <div className="flex items-center gap-2 text-sm font-bold mb-2"><AlertTriangle className="h-5 w-5" /> باب للقراءة المسؤولة</div>
                      <h2 className="text-3xl md:text-4xl font-bold">{tragedyChapter.title}</h2>
                      <p className="mt-2 text-white/90">{tragedyChapter.subtitle}</p>
                    </div>
                  </div>
                  <CardContent className="p-6 md:p-8">
                    <div className="bg-amber-50 border-r-4 border-amber-400 p-4 rounded-xl text-amber-950 leading-relaxed mb-6">
                      <strong>تنبيه تحريري:</strong> لا ينشر هذا الباب أسماء أو أسباب وفاة غير موثقة، ولا يربط الانتحار أو الإدمان أو المرض بسبب واحد. الهدف هو التوعية بالصحة والخصوصية والوقاية واحترام كرامة الأشخاص.
                    </div>
                    <div className="flex flex-wrap gap-3 mb-8">
                      <Button variant="outline" className="rounded-xl" onClick={() => setActiveSection('home')}>العودة إلى الرئيسية</Button>
                      <Button variant="outline" className="rounded-xl" onClick={() => setActiveSection('pornMediaLiteracy')}>الرجوع إلى باب الوعي الإعلامي</Button>
                      <Button variant="outline" className="rounded-xl" onClick={() => setActiveSection('sexualDiseases')}>الانتقال إلى باب الأمراض الجنسية</Button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                      {tragedyChapter.articles.map(article => (
                        <ArticleCard key={article.id} article={{ ...article, category: tragedyChapter.title }} onViewDetails={handleViewArticleDetails} />
                      ))}
                    </div>
                    <div className="mt-8 pt-6 border-t border-gray-100 text-sm text-gray-600 leading-relaxed">
                      {tragedyChapter.sourceNote}
                      <div className="mt-4 flex flex-wrap gap-3">{tragedyChapter.sources.map(source => <a key={source.url} href={source.url} target="_blank" rel="noreferrer" className="text-indigo-700 hover:underline">{source.label}</a>)}</div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {activeSection === 'tips' && (
              <div className="max-w-4xl mx-auto space-y-8">
                <div className="grid md:grid-cols-2 gap-6">
                  {getArticlesForSection('tips').map(article => (
                    <ArticleCard key={article.id} article={article} onViewDetails={handleViewArticleDetails} />
                  ))}
                </div>
              </div>
            )}

            {activeSection === 'faq' && (
              <div className="max-w-4xl mx-auto space-y-6">
                {getArticlesForSection('faq').map(article => (
                  <Card key={article.id} className="cursor-pointer hover:shadow-md transition-all" onClick={() => handleViewArticleDetails(article)}>
                    <CardHeader className="flex flex-row items-center justify-between p-6">
                      <CardTitle className="text-lg text-blue-700">{article.title}</CardTitle>
                      <HelpCircle className="h-5 w-5 text-blue-400" />
                    </CardHeader>
                  </Card>
                ))}
              </div>
            )}
          </div>

          {/* Sidebar Ads */}
          <aside className="hidden lg:block w-80 space-y-6">
            <div className="sticky top-24 space-y-6">
              <AdSpace location="sidebar" />
              <Card className="bg-gradient-to-br from-pink-500 to-purple-600 text-white border-none rounded-3xl overflow-hidden">
                <CardContent className="p-6 space-y-4">
                  <Star className="h-10 w-10 opacity-50" />
                  <h4 className="text-xl font-bold">دليل الليلة الأولى</h4>
                  <p className="text-sm opacity-90">احصل على نسختك المجانية من الدليل الشامل لليلة العمر.</p>
                  <Button className="w-full bg-white text-pink-600 hover:bg-pink-50 font-bold">تحميل الدليل</Button>
                </CardContent>
              </Card>
            </div>
          </aside>
        </div>
      </main>

      <AdSpace location="footer" />

      <footer className="bg-gray-900 text-gray-400 py-16 mt-16">
        <div className="container mx-auto px-4 grid md:grid-cols-3 gap-12">
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <Heart className="h-6 w-6 text-pink-500" />
              <span className="text-2xl font-bold text-white">دليل التثقيف الزواجي</span>
            </div>
            <p className="leading-relaxed">
              المنصة العربية الأولى المتخصصة في التثقيف الزواجي العلمي المحترم. نهدف لبناء أسر متماسكة ومجتمع صحي.
            </p>
          </div>
          <div>
            <h4 className="text-white font-bold mb-6">روابط سريعة</h4>
            <ul className="grid grid-cols-2 gap-4">
              {sections.map(s => (
                <li key={s.id}>
                  <button onClick={() => setActiveSection(s.id)} className="hover:text-white transition-colors">{s.title}</button>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-white font-bold mb-6">تنبيه قانوني</h4>
            <p className="text-sm leading-relaxed">
              جميع المعلومات الطبية والتعليمية الواردة في هذا الموقع هي لأغراض التوعية فقط، ولا تغني عن استشارة الأطباء المختصين في الحالات الطبية.
            </p>
          </div>
        </div>
        <div className="container mx-auto px-4 border-t border-gray-800 mt-12 pt-8 text-center text-sm">
          جميع الحقوق محفوظة © 2026 - دليل التثقيف الزواجي
        </div>
      </footer>

      {/* Modals */}
      <PositionModal position={selectedPosition} isOpen={isPositionModalOpen} onClose={() => setIsPositionModalOpen(false)} />
      <ArticleModal 
        article={selectedArticle} 
        articles={[...articles, ...sexualDiseasesChapter.articles.map(article => ({ ...article, category: sexualDiseasesChapter.title })), ...pornMediaLiteracyChapter.articles.map(article => ({ ...article, category: pornMediaLiteracyChapter.title })), ...tragedyChapter.articles.map(article => ({ ...article, category: tragedyChapter.title }))]}
        isOpen={isArticleModalOpen} 
        onClose={() => setIsArticleModalOpen(false)} 
        onViewArticle={(a) => {
          setSelectedArticle(a)
          setIsArticleModalOpen(true)
        }}
      />
      <AdminPanel isOpen={isAdminPanelOpen} onClose={() => setIsAdminPanelOpen(false)} />
    </div>
  )
}

export default App
