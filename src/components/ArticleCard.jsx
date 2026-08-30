import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { BookOpen } from 'lucide-react'
import { assetPath } from '@/lib/assetPath.js'

const ArticleCard = ({ article, onViewDetails }) => {
  return (
    <Card className="flex flex-col h-full hover:shadow-xl transition-all duration-300 border-t-4 border-t-green-500">
      <div className="relative h-48 overflow-hidden">
        <img 
          src={assetPath(article.image)} 
          alt={article.title}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
        />
        <div className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
          {article.category.split(':')[0]}
        </div>
      </div>
      <CardHeader className="flex-grow">
        <CardTitle className="text-xl text-gray-800 line-clamp-2">{article.title}</CardTitle>
        <CardDescription className="text-sm text-gray-500 mt-2">
          {article.keywords}
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="text-gray-600 text-sm line-clamp-3 mb-4">
          {article.description}
        </p>
        <Button 
          onClick={() => onViewDetails(article)}
          className="w-full bg-green-600 hover:bg-green-700 text-white"
        >
          <BookOpen className="h-4 w-4 ml-2" />
          اقرأ المقال كاملاً
        </Button>
      </CardContent>
    </Card>
  )
}

export default ArticleCard
