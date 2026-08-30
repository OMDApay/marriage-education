import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Eye, Heart } from 'lucide-react'

const PositionCard = ({ position, onViewDetails }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow duration-300 group">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-blue-700 group-hover:text-blue-800 transition-colors">
            {position.title}
          </CardTitle>
          <Heart className="h-5 w-5 text-gray-400 group-hover:text-pink-500 transition-colors" />
        </div>
        <CardDescription className="text-sm text-gray-600">
          {position.category}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {position.image && (
          <div className="relative overflow-hidden rounded-lg bg-gray-100">
            <img 
              src={position.image} 
              alt={position.title}
              className="w-full h-32 object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300" />
          </div>
        )}
        
        <p className="text-sm text-gray-700 line-clamp-3">
          {position.description}
        </p>
        
        <div className="flex flex-wrap gap-2">
          {position.tags && position.tags.map((tag, index) => (
            <span 
              key={index}
              className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
        
        <Button 
          onClick={() => onViewDetails(position)}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white"
          size="sm"
        >
          <Eye className="h-4 w-4 mr-2" />
          عرض التفاصيل
        </Button>
      </CardContent>
    </Card>
  )
}

export default PositionCard

