import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { BookOpen, Share2, Printer, X } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { assetPath } from '@/lib/assetPath.js'

const ArticleModal = ({ article, articles = [], isOpen, onClose, onViewArticle }) => {
  if (!article) return null

  const sameChapterArticles = articles.filter(a => a.category === article.category)
  const currentIndex = sameChapterArticles.findIndex(a => a.id === article.id)
  const previousArticle = currentIndex > 0 ? sameChapterArticles[currentIndex - 1] : null
  const nextArticle = currentIndex >= 0 && currentIndex < sameChapterArticles.length - 1 ? sameChapterArticles[currentIndex + 1] : null
  const articleTerms = new Set((article.keywords || '').split(/[،,]/).map(term => term.trim()).filter(Boolean))
  const keywordScore = (candidate) => (candidate.keywords || '').split(/[،,]/).map(term => term.trim()).filter(Boolean).reduce((score, term) => score + (articleTerms.has(term) ? 2 : 0), 0)
  const sameChapterRelated = sameChapterArticles
    .filter(a => a.id !== article.id)
    .slice(0, 2)
  const crossChapterRelated = articles
    .filter(a => a.id !== article.id && a.category !== article.category)
    .map(a => ({ article: a, score: keywordScore(a) }))
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 1)
    .map(item => item.article)
  const relatedArticles = [...sameChapterRelated, ...crossChapterRelated]

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto relative" dir="rtl">
        {/* زر إغلاق بارز وواضح جداً */}
        <button 
          onClick={onClose}
          className="absolute left-4 top-4 bg-gray-100 hover:bg-pink-500 hover:text-white p-2 rounded-full transition-all z-50 shadow-md flex items-center justify-center"
          title="إغلاق النافذة"
        >
          <X className="h-6 w-6" />
        </button>

        <DialogHeader className="pr-12">
          <div className="flex justify-between items-start mb-4">
            <Badge variant="outline" className="text-green-600 border-green-600">
              {article.category}
            </Badge>
            <div className="flex gap-2">
              <Button variant="ghost" size="icon" onClick={() => window.print()} title="طباعة">
                <Printer className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <DialogTitle className="text-3xl font-bold text-gray-800 text-right leading-tight">
            {article.title}
          </DialogTitle>
          <DialogDescription className="text-right text-lg text-gray-500 mt-2">
            {article.keywords}
          </DialogDescription>
        </DialogHeader>

        <div className="mt-6 space-y-6">
          <img 
            src={assetPath(article.image)} 
            alt={article.title}
            className="w-full h-80 object-cover rounded-2xl shadow-lg"
          />
          
          <div className="bg-green-50 p-6 rounded-2xl border-r-4 border-green-500">
            <h4 className="text-xl font-bold text-green-800 mb-2">ملخص المقال:</h4>
            <p className="text-green-700 leading-relaxed text-lg">
              {article.description}
            </p>
          </div>

          <div className="prose prose-lg max-w-none text-right">
            <div className="text-gray-700 leading-loose whitespace-pre-wrap text-xl">
              {article.content}
            </div>
          </div>

          <div className="border-t pt-6 mt-8 flex flex-col gap-4">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 rounded-2xl bg-indigo-50 border border-indigo-100 p-4">
              <Button
                variant="outline"
                disabled={!previousArticle}
                onClick={() => previousArticle && onViewArticle(previousArticle)}
                className="w-full sm:w-auto rounded-xl border-indigo-200 text-indigo-700 disabled:opacity-40"
              >
                ← السابق
              </Button>
              <span className="text-sm font-medium text-indigo-800">المقال {currentIndex + 1} من {sameChapterArticles.length}</span>
              <Button
                variant="outline"
                disabled={!nextArticle}
                onClick={() => nextArticle && onViewArticle(nextArticle)}
                className="w-full sm:w-auto rounded-xl border-indigo-200 text-indigo-700 disabled:opacity-40"
              >
                التالي →
              </Button>
            </div>

            <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>
              <h4 className="text-lg font-bold text-gray-800 mb-1">نصيحة إضافية:</h4>
              <p className="text-gray-600 italic text-sm">
                هذه المعلومات طبية تعليمية وتهدف لزيادة الوعي الصحي والزواجي.
              </p>
            </div>
            <Button 
              onClick={onClose}
              className="bg-pink-600 hover:bg-pink-500 text-white px-8 py-3 rounded-xl font-bold shadow-md"
            >
              إغلاق المقال
            </Button>
            </div>
          </div>

          {relatedArticles.length > 0 && (
            <div className="border-t pt-8 mt-8">
              <h4 className="text-2xl font-bold text-gray-800 mb-6">مقالات ذات صلة ومكملة:</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {relatedArticles.map(rel => (
                  <div 
                    key={rel.id} 
                    className="group cursor-pointer bg-gray-50 rounded-2xl overflow-hidden border border-gray-100 hover:shadow-xl transition-all"
                    onClick={() => onViewArticle(rel)}
                  >
                    <img src={assetPath(rel.image)} alt={rel.title} className="w-full h-36 object-cover group-hover:scale-105 transition-transform" />
                    <div className="p-4">
                      <h5 className="font-bold text-sm text-gray-800 line-clamp-2 group-hover:text-pink-600">{rel.title}</h5>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default ArticleModal
